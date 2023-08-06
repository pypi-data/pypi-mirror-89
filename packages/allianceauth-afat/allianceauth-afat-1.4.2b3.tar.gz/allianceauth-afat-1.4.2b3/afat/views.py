# -*- coding: utf-8 -*-

"""
the views
"""

from collections import OrderedDict

from datetime import datetime, timedelta

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.crypto import get_random_string

from esi.decorators import token_required
from esi.models import Token

from afat import __title__
from afat.forms import (
    AFatLinkForm,
    AFatManualFatForm,
    AFatClickFatForm,
    FatLinkEditForm,
)
from afat.helper.views_helper import (
    convert_fatlinks_to_dict,
    convert_fats_to_dict,
    get_random_rgba_color,
)
from afat.models import (
    AFat,
    ClickAFatDuration,
    AFatLink,
    ManualAFat,
    AFatDelLog,
    AFatLinkType,
)
from afat.permissions import get_user_permissions
from afat.providers import esi
from afat.tasks import get_or_create_char, process_fats
from afat.utils import LoggerAddTag

from allianceauth.authentication.decorators import permissions_required
from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from allianceauth.eveonline.providers import provider
from allianceauth.services.hooks import get_extension_logger


logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required()
@permission_required("afat.basic_access")
def dashboard(request: WSGIRequest) -> HttpResponse:
    """
    dashboard
    :param request:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(request.user)

    msg = None

    if "msg" in request.session:
        msg = request.session.pop("msg")

    characters_by_user = CharacterOwnership.objects.filter(user=request.user)
    characters = list()

    for users_character in characters_by_user:
        character_fat = AFat.objects.filter(character=users_character.character)

        if character_fat.count() > 0:
            characters.append(users_character.character)

    context = {"characters": characters, "msg": msg, "permissions": permissions}

    logger.info("Module called by {user}".format(user=request.user))

    return render(request, "afat/dashboard.html", context)


@login_required
@permission_required("afat.basic_access")
def dashboard_fats_data(request: WSGIRequest, charid: int) -> JsonResponse:
    """
    ajax call
    get fats for dashboard view
    :param request:
    :param charid:
    """

    character = EveCharacter.objects.get(character_id=charid)

    fats = (
        AFat.objects.filter(character=character)
        .order_by("afatlink__afattime")
        .reverse()[:10]
    )

    character_fat_rows = [
        convert_fats_to_dict(request=request, fat=fat) for fat in fats
    ]

    return JsonResponse(character_fat_rows, safe=False)


@login_required
@permission_required("afat.basic_access")
def dashboard_links_data(request: WSGIRequest) -> JsonResponse:
    """
    ajax call
    get recent fat links for the dashboard datatable
    :param request:
    """

    fatlinks = AFatLink.objects.order_by("-afattime").annotate(
        number_of_fats=Count("afat", filter=Q(afat__deleted_at__isnull=True))
    )[:10]

    fatlink_rows = [
        convert_fatlinks_to_dict(request=request, fatlink=fatlink)
        for fatlink in fatlinks
    ]

    return JsonResponse(fatlink_rows, safe=False)


@login_required()
@permission_required("afat.basic_access")
def stats(request: WSGIRequest, year: int = None) -> HttpResponse:
    """
    statistics main view
    :type year: string
    :param request:
    :param year:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(request.user)

    if year is None:
        year = datetime.now().year

    if request.user.has_perm("afat.stats_corp_other"):
        corps = EveCorporationInfo.objects.all()
        alliances = EveAllianceInfo.objects.all()
        data = {"No Alliance": []}

        for alliance in alliances:
            data[alliance.alliance_name] = [alliance.alliance_id]

        for corp in corps:
            if corp.alliance is None:
                data["No Alliance"].append((corp.corporation_id, corp.corporation_name))
            else:
                data[corp.alliance.alliance_name].append(
                    (corp.corporation_id, corp.corporation_name)
                )
    elif request.user.has_perm("afat.stats_corp_own"):
        data = [
            (
                request.user.profile.main_character.corporation_id,
                request.user.profile.main_character.corporation_name,
            )
        ]
    else:
        data = None

    chars = CharacterOwnership.objects.filter(user=request.user)
    months = list()

    for char in chars:
        char_fats = AFat.objects.filter(afatlink__afattime__year=year)
        char_stats = {}

        char_has_fats = False

        for i in range(1, 13):
            char_fat_count = (
                char_fats.filter(afatlink__afattime__month=i)
                .filter(character__id=char.character.id)
                .count()
            )

            if char_fat_count > 0:
                char_stats[str(i)] = char_fat_count
                char_has_fats = True

        if char_has_fats is True:
            char_l = [char.character.character_name]
            char_l.append(char_stats)
            char_l.append(char.character.character_id)
            months.append(char_l)

    context = {
        "data": data,
        "charstats": months,
        "year": year,
        "year_current": datetime.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "permissions": permissions,
    }

    logger.info("Statistics overview called by {user}".format(user=request.user))

    return render(request, "afat/stats_main.html", context)


@login_required()
@permission_required("afat.basic_access")
def stats_char(
    request: WSGIRequest, charid: int, year: int = None, month: int = None
) -> HttpResponse:
    """
    character statistics view
    :param request:
    :param charid:
    :param month:
    :param year:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(request.user)

    character = EveCharacter.objects.get(character_id=charid)
    valid = [
        char.character for char in CharacterOwnership.objects.filter(user=request.user)
    ]

    if character not in valid and not request.user.has_perm("afat.stats_char_other"):
        request.session["msg"] = (
            "warning",
            "You do not have permission to view statistics for this character.",
        )

        return redirect("afat:dashboard")

    if not month or not year:
        request.session["msg"] = ("danger", "Date information not complete!")

        return redirect("afat:dashboard")

    fats = AFat.objects.filter(
        character__character_id=charid,
        afatlink__afattime__month=month,
        afatlink__afattime__year=year,
    )

    # Data for Ship Type Pie Chart
    data_ship_type = {}

    for fat in fats:
        if fat.shiptype in data_ship_type.keys():
            continue

        data_ship_type[fat.shiptype] = fats.filter(shiptype=fat.shiptype).count()

    colors = []

    for _ in data_ship_type.keys():
        bg_color_str = get_random_rgba_color()
        colors.append(bg_color_str)

    data_ship_type = [
        # ship type can be None, so we need to convert to string here
        list(str(key) for key in data_ship_type.keys()),
        list(data_ship_type.values()),
        colors,
    ]

    # Data for by Time Line Chart
    data_time = {}

    for i in range(0, 24):
        data_time[i] = fats.filter(afatlink__afattime__hour=i).count()

    data_time = [
        list(data_time.keys()),
        list(data_time.values()),
        [get_random_rgba_color()],
    ]

    context = {
        "character": character,
        "month": month,
        "month_current": datetime.now().month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "year": year,
        "year_current": datetime.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_ship_type": data_ship_type,
        "data_time": data_time,
        "fats": fats,
        "permissions": permissions,
    }

    logger.info("Character statistics called by {user}".format(user=request.user))

    return render(request, "afat/char_stat.html", context)


@login_required()
@permissions_required(("afat.stats_corp_own", "afat.stats_corp_other"))
def stats_corp(
    request: WSGIRequest, corpid: int, year: int = None, month: int = None
) -> HttpResponse:
    """
    corp statistics view
    :param request:
    :param corpid:
    :param month:
    :param year:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(request.user)

    if not year:
        year = datetime.now().year

    # Check character has permission to view other corp stats
    if int(request.user.profile.main_character.corporation_id) != int(corpid):
        if not request.user.has_perm("afat.stats_corp_other"):
            request.session["msg"] = (
                "warning",
                "You do not have permission to view statistics for that corporation.",
            )

            return redirect("afat:dashboard")

    corp = EveCorporationInfo.objects.get(corporation_id=corpid)
    corp_name = corp.corporation_name

    if not month:
        months = []

        for i in range(1, 13):
            corp_fats = AFat.objects.filter(
                character__corporation_id=corpid,
                afatlink__afattime__month=i,
                afatlink__afattime__year=year,
            ).count()

            avg_fats = corp_fats / corp.member_count

            if corp_fats > 0:
                months.append((i, corp_fats, round(avg_fats, 2)))

        context = {
            "corporation": corp.corporation_name,
            "months": months,
            "corpid": corpid,
            "year": year,
            "year_current": datetime.now().year,
            "year_prev": int(year) - 1,
            "year_next": int(year) + 1,
            "type": 0,
            "permissions": permissions,
        }

        return render(request, "afat/date_select.html", context)

    fats = AFat.objects.filter(
        afatlink__afattime__month=month,
        afatlink__afattime__year=year,
        character__corporation_id=corpid,
    )

    characters = EveCharacter.objects.filter(corporation_id=corpid)

    # Data for Stacked Bar Graph
    # (label, color, [list of data for stack])
    data = {}

    for fat in fats:
        if fat.shiptype in data.keys():
            continue

        data[fat.shiptype] = {}

    chars = []

    for fat in fats:
        if fat.character.character_name in chars:
            continue

        chars.append(fat.character.character_name)

    for key, ship_type in data.items():
        for char in chars:
            ship_type[char] = 0

    for fat in fats:
        data[fat.shiptype][fat.character.character_name] += 1

    data_stacked = []

    for key, value in data.items():
        stack = list()
        stack.append(key)
        stack.append(get_random_rgba_color())
        stack.append([])

        data_ = stack[2]

        for char in chars:
            data_.append(value[char])

        stack.append(data_)
        data_stacked.append(tuple(stack))

    data_stacked = [chars, data_stacked]

    # Data for By Time
    data_time = {}

    for i in range(0, 24):
        data_time[i] = fats.filter(afatlink__afattime__hour=i).count()

    data_time = [
        list(data_time.keys()),
        list(data_time.values()),
        [get_random_rgba_color()],
    ]

    # Data for By Weekday
    data_weekday = []

    for i in range(1, 8):
        data_weekday.append(fats.filter(afatlink__afattime__week_day=i).count())

    data_weekday = [
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        data_weekday,
        [get_random_rgba_color()],
    ]

    chars = {}

    for char in characters:
        fat_c = fats.filter(character_id=char.id).count()
        chars[char.character_name] = (fat_c, char.character_id)

    context = {
        "corp": corp,
        "corporation": corp.corporation_name,
        "month": month,
        "month_current": datetime.now().month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "year": year,
        "year_current": datetime.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_stacked": data_stacked,
        "data_time": data_time,
        "data_weekday": data_weekday,
        "chars": chars,
        "permissions": permissions,
    }

    logger.info(
        "Corporation statistics for {corp_name} called by {user}".format(
            corp_name=corp_name, user=request.user
        )
    )

    return render(request, "afat/corp_stat.html", context)


@login_required()
@permission_required("afat.stats_corp_other")
def stats_alliance(
    request: WSGIRequest, allianceid: int, year: int = None, month: int = None
) -> HttpResponse:
    """
    alliance statistics view
    :param request:
    :param allianceid:
    :param month:
    :param year:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(request.user)

    if not year:
        year = datetime.now().year

    if allianceid == "000":
        allianceid = None

    if allianceid is not None:
        ally = EveAllianceInfo.objects.get(alliance_id=allianceid)
        alliance_name = ally.alliance_name
    else:
        ally = None
        alliance_name = "No Alliance"

    if not month:
        months = []

        for i in range(1, 13):
            ally_fats = AFat.objects.filter(
                character__alliance_id=allianceid,
                afatlink__afattime__month=i,
                afatlink__afattime__year=year,
            ).count()

            if ally_fats > 0:
                months.append((i, ally_fats))

        context = {
            "corporation": alliance_name,
            "months": months,
            "corpid": allianceid,
            "year": year,
            "year_current": datetime.now().year,
            "year_prev": int(year) - 1,
            "year_next": int(year) + 1,
            "type": 1,
            "permissions": permissions,
        }

        return render(request, "afat/date_select.html", context)

    if not month or not year:
        request.session["msg"] = ("danger", "Date information incomplete.")

        return redirect("afat:dashboard")

    fats = AFat.objects.filter(
        character__alliance_id=allianceid,
        afatlink__afattime__month=month,
        afatlink__afattime__year=year,
    )

    corporations = EveCorporationInfo.objects.filter(alliance=ally)

    # Data for Ship Type Pie Chart
    data_ship_type = {}

    for fat in fats:
        if fat.shiptype in data_ship_type.keys():
            continue

        data_ship_type[fat.shiptype] = fats.filter(shiptype=fat.shiptype).count()

    colors = []

    for _ in data_ship_type.keys():
        bg_color_str = get_random_rgba_color()
        colors.append(bg_color_str)

    data_ship_type = [
        # ship type can be None, so we need to convert to string here
        list(str(key) for key in data_ship_type.keys()),
        list(data_ship_type.values()),
        colors,
    ]

    # Fats by corp and ship type?
    data = {}

    for fat in fats:
        if fat.shiptype in data.keys():
            continue

        data[fat.shiptype] = {}

    corps = []

    for fat in fats:
        if fat.character.corporation_name in corps:
            continue

        corps.append(fat.character.corporation_name)

    for key, ship_type in data.items():
        for corp in corps:
            ship_type[corp] = 0

    for fat in fats:
        data[fat.shiptype][fat.character.corporation_name] += 1

    if None in data.keys():
        data["Unknown"] = data[None]
        data.pop(None)

    data_stacked = []

    for key, value in data.items():
        stack = list()
        stack.append(key)
        stack.append(get_random_rgba_color())
        stack.append([])

        data_ = stack[2]

        for corp in corps:
            data_.append(value[corp])

        stack.append(data_)
        data_stacked.append(tuple(stack))

    data_stacked = [corps, data_stacked]

    # Avg fats by corp
    data_avgs = {}

    for corp in corporations:
        c_fats = fats.filter(character__corporation_id=corp.corporation_id).count()
        avg = c_fats / corp.member_count
        data_avgs[corp.corporation_name] = round(avg, 2)

    data_avgs = OrderedDict(sorted(data_avgs.items(), key=lambda x: x[1], reverse=True))
    data_avgs = [
        list(data_avgs.keys()),
        list(data_avgs.values()),
        get_random_rgba_color(),
    ]

    # Fats by Time
    data_time = {}

    for i in range(0, 24):
        data_time[i] = fats.filter(afatlink__afattime__hour=i).count()

    data_time = [
        list(data_time.keys()),
        list(data_time.values()),
        [get_random_rgba_color()],
    ]

    # Fats by weekday
    data_weekday = []

    for i in range(1, 8):
        data_weekday.append(fats.filter(afatlink__afattime__week_day=i).count())

    data_weekday = [
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        data_weekday,
        [get_random_rgba_color()],
    ]

    # Corp list
    corps = {}

    for corp in corporations:
        c_fats = fats.filter(character__corporation_id=corp.corporation_id).count()
        avg = c_fats / corp.member_count
        corps[corp] = (corp.corporation_id, c_fats, round(avg, 2))

    corps = OrderedDict(sorted(corps.items(), key=lambda x: x[1][2], reverse=True))

    context = {
        "alliance": alliance_name,
        "ally": ally,
        "month": month,
        "month_current": datetime.now().month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "year": year,
        "year_current": datetime.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_stacked": data_stacked,
        "data_avgs": data_avgs,
        "data_time": data_time,
        "data_weekday": data_weekday,
        "corps": corps,
        "data_ship_type": data_ship_type,
        "permissions": permissions,
    }

    logger.info(
        "Alliance statistics for {alliance_name} called by {user}".format(
            alliance_name=alliance_name, user=request.user
        )
    )

    return render(request, "afat/ally_stat.html", context)


@login_required()
@permission_required("afat.basic_access")
def links(request: WSGIRequest, year: int = None) -> HttpResponse:
    """
    fatlinks view
    :param year:
    :param request:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(request.user)

    if year is None:
        year = datetime.now().year

    msg = None

    if "msg" in request.session:
        msg = request.session.pop("msg")

    context = {
        "msg": msg,
        "year": year,
        "year_current": datetime.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "permissions": permissions,
    }

    logger.info("FAT link list called by {user}".format(user=request.user))

    return render(request, "afat/fat_list.html", context)


@login_required()
@permission_required("afat.basic_access")
def links_data(request: WSGIRequest, year: int = None) -> JsonResponse:
    """
    fatlinks view
    :param year:
    :param request:
    :return:
    """

    if year is None:
        year = datetime.now().year

    fatlinks = (
        AFatLink.objects.filter(afattime__year=year)
        .order_by("-afattime")
        .annotate(number_of_fats=Count("afat", filter=Q(afat__deleted_at__isnull=True)))
    )

    fatlink_rows = [
        convert_fatlinks_to_dict(request=request, fatlink=fatlink)
        for fatlink in fatlinks
    ]

    return JsonResponse(fatlink_rows, safe=False)


@login_required()
@permissions_required(("afat.manage_afat", "afat.add_afatlink"))
def link_add(request: WSGIRequest) -> HttpResponse:
    """
    add fatlink view
    :param request:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(request.user)

    msg = None

    if "msg" in request.session:
        msg = request.session.pop("msg")

    link_types = AFatLinkType.objects.filter(
        is_enabled=True,
    ).order_by("name")

    has_open_esi_fleet = AFatLink.objects.filter(
        creator=request.user, is_esilink=True, is_registered_on_esi=True
    ).exists()

    context = {
        "link_types": link_types,
        "msg": msg,
        "permissions": permissions,
        "has_open_esi_fleet": has_open_esi_fleet,
    }

    logger.info("Add FAT link view called by {user}".format(user=request.user))

    return render(request, "afat/addlink.html", context)


@login_required()
@permissions_required(("afat.manage_afat", "afat.add_afatlink"))
def link_create_click(request: WSGIRequest):
    """
    create fatlink helper
    :param request:
    :return:
    """

    if request.method == "POST":
        form = AFatClickFatForm(request.POST)

        if form.is_valid():
            fatlink_hash = get_random_string(length=30)

            link = AFatLink()
            link.fleet = form.cleaned_data["name"]

            if (
                form.cleaned_data["type"] is not None
                and form.cleaned_data["type"] != -1
            ):
                link.link_type = AFatLinkType.objects.get(id=form.cleaned_data["type"])

            link.creator = request.user
            link.hash = fatlink_hash
            link.save()

            dur = ClickAFatDuration()
            dur.fleet = AFatLink.objects.get(hash=fatlink_hash)
            dur.duration = form.cleaned_data["duration"]
            dur.save()

            request.session[
                "{fatlink_hash}-creation-code".format(fatlink_hash=fatlink_hash)
            ] = 202

            logger.info(
                "FAT link {fatlink_hash} with name {name} and a "
                "duration of {duration} minutes was created by {user}".format(
                    fatlink_hash=fatlink_hash,
                    name=form.cleaned_data["name"],
                    duration=form.cleaned_data["duration"],
                    user=request.user,
                )
            )

            return redirect("afat:link_edit", fatlink_hash=fatlink_hash)

        request.session["msg"] = [
            "danger",
            (
                "Something went wrong when attempting to submit your"
                " clickable FAT Link."
            ),
        ]
        return redirect("afat:dashboard")

    request.session["msg"] = [
        "warning",
        (
            'You must fill out the form on the "Add FAT Link" '
            "page to create a clickable FAT Link"
        ),
    ]

    return redirect("afat:dashboard")


@login_required()
@permissions_required(("afat.manage_afat", "afat.add_afatlink"))
@token_required(scopes=["esi-fleets.read_fleet.v1"])
def link_create_esi(request: WSGIRequest, token, fatlink_hash: str):
    """
    helper: create ESI link
    :param request:
    :param token:
    :param fatlink_hash:
    :return:
    """

    # Check if there is a fleet
    try:
        required_scopes = ["esi-fleets.read_fleet.v1"]
        esi_token = Token.get_token(token.character_id, required_scopes)

        fleet_from_esi = esi.client.Fleets.get_characters_character_id_fleet(
            character_id=token.character_id, token=esi_token.valid_access_token()
        ).result()
    except Exception:
        # Not in a fleet
        request.session["msg"] = [
            "warning",
            "To use the ESI function, you neeed to be in fleet and you need to be "
            "the fleet boss! You can create a clickable FAT link and share it, "
            "if you like.",
        ]

        # return to "Add FAT Link" view
        return redirect("afat:link_add")

    # Check if we deal with the fleet boss here
    try:
        esi_fleet_member = esi.client.Fleets.get_fleets_fleet_id_members(
            fleet_id=fleet_from_esi["fleet_id"],
            token=esi_token.valid_access_token(),
        ).result()
    except Exception:
        request.session["msg"] = [
            "warning",
            "Not Fleet Boss! Only the fleet boss can utilize the ESI function. "
            "You can create a clickable FAT link and share it, if you like.",
        ]

        # return to "Add FAT Link" view
        return redirect("afat:link_add")

    creator_character = EveCharacter.objects.get(character_id=token.character_id)

    # create the fatlink
    fatlink = AFatLink(
        fleet=request.session["fatlink_form__name"],
        creator=request.user,
        character=creator_character,
        hash=fatlink_hash,
        is_esilink=True,
        is_registered_on_esi=True,
        esi_fleet_id=fleet_from_esi["fleet_id"],
    )

    # add fleet type if there is any
    if (
        request.session["fatlink_form__type"] is not None
        and request.session["fatlink_form__type"] != -1
    ):
        fatlink.link_type = AFatLinkType.objects.get(
            id=request.session["fatlink_form__type"]
        )

    # save it
    fatlink.save()

    # clear session
    # request.session["fatlink_form__name"] = None
    # request.session["fatlink_form__type"] = None
    del request.session["fatlink_form__name"]
    del request.session["fatlink_form__type"]

    # process fleet members
    process_fats.delay(
        data_list=esi_fleet_member, data_source="esi", fatlink_hash=fatlink_hash
    )

    request.session[
        "{fatlink_hash}-creation-code".format(fatlink_hash=fatlink_hash)
    ] = 200

    logger.info(
        "ESI FAT link {fatlink_hash} created by {user}".format(
            fatlink_hash=fatlink_hash, user=request.user
        )
    )

    return redirect("afat:link_edit", fatlink_hash=fatlink_hash)


@login_required()
def create_esi_fat(request: WSGIRequest):
    """
    create ESI fat helper
    :param request:
    :return:
    """

    fatlink_form = AFatLinkForm(request.POST)

    if fatlink_form.is_valid():
        fatlink_hash = get_random_string(length=30)

        request.session["fatlink_form__name"] = fatlink_form.cleaned_data["name_esi"]
        request.session["fatlink_form__type"] = fatlink_form.cleaned_data["type_esi"]

        return redirect("afat:link_create_esi", fatlink_hash=fatlink_hash)

    request.session["msg"] = [
        "danger",
        "Something went wrong when attempting to submit your ESI FAT Link.",
    ]

    return redirect("afat:dashboard")


@login_required()
@permission_required("afat.basic_access")
@token_required(
    scopes=[
        "esi-location.read_location.v1",
        "esi-location.read_ship_type.v1",
        "esi-location.read_online.v1",
    ]
)
def click_link(request: WSGIRequest, token, fatlink_hash: str = None):
    """
    click fatlink helper
    :param request:
    :param token:
    :param fatlink_hash:
    :return:
    """
    if fatlink_hash is None:
        request.session["msg"] = ["warning", "No FAT link hash provided."]

        return redirect("afat:dashboard")

    try:
        try:
            fleet = AFatLink.objects.get(hash=fatlink_hash)
        except AFatLink.DoesNotExist:
            request.session["msg"] = ["warning", "The hash provided is not valid."]

            return redirect("afat:dashboard")

        dur = ClickAFatDuration.objects.get(fleet=fleet)
        now = timezone.now() - timedelta(minutes=dur.duration)

        if now >= fleet.afattime:
            request.session["msg"] = [
                "warning",
                (
                    "Sorry, that FAT Link is expired. If you were on that fleet, "
                    "contact your FC about having your FAT manually added."
                ),
            ]

            return redirect("afat:dashboard")

        character = EveCharacter.objects.get(character_id=token.character_id)

        try:
            required_scopes = [
                "esi-location.read_location.v1",
                "esi-location.read_online.v1",
                "esi-location.read_ship_type.v1",
            ]
            esi_token = Token.get_token(token.character_id, required_scopes)

            # check if character is online
            character_online = esi.client.Location.get_characters_character_id_online(
                character_id=token.character_id, token=esi_token.valid_access_token()
            ).result()

            if character_online["online"] is True:
                # character location
                location = esi.client.Location.get_characters_character_id_location(
                    character_id=token.character_id,
                    token=esi_token.valid_access_token(),
                ).result()

                # current ship
                ship = esi.client.Location.get_characters_character_id_ship(
                    character_id=token.character_id,
                    token=esi_token.valid_access_token(),
                ).result()

                # system information
                system = esi.client.Universe.get_universe_systems_system_id(
                    system_id=location["solar_system_id"]
                ).result()["name"]

                ship_name = provider.get_itemtype(ship["ship_type_id"]).name

                try:
                    fat = AFat(
                        afatlink=fleet,
                        character=character,
                        system=system,
                        shiptype=ship_name,
                    )
                    fat.save()

                    if fleet.fleet is not None:
                        name = fleet.fleet
                    else:
                        name = fleet.hash

                    request.session["msg"] = [
                        "success",
                        (
                            "FAT registered for {character_name} "
                            "at {fleet_name}".format(
                                character_name=character.character_name, fleet_name=name
                            )
                        ),
                    ]

                    logger.info(
                        "Fleetparticipation for fleet {fleet_name} "
                        "registered for pilot {character_name}".format(
                            fleet_name=name, character_name=character.character_name
                        )
                    )

                    return redirect("afat:dashboard")
                except Exception:
                    request.session["msg"] = [
                        "warning",
                        (
                            "A FAT already exists for the selected character "
                            "({character_name}) and fleet combination.".format(
                                character_name=character.character_name
                            )
                        ),
                    ]

                    return redirect("afat:dashboard")
            else:
                request.session["msg"] = [
                    "warning",
                    (
                        "Cannot register the fleet participation for {character_name}. "
                        "The character needs to be online.".format(
                            character_name=character.character_name
                        )
                    ),
                ]

                return redirect("afat:dashboard")
        except Exception:
            request.session["msg"] = [
                "warning",
                (
                    "There was an issue with the token for {character_name}. "
                    "Please try again.".format(character_name=character.character_name)
                ),
            ]

            return redirect("afat:dashboard")
    except Exception:
        request.session["msg"] = [
            "warning",
            "The hash provided is not for a clickable FAT Link.",
        ]

        return redirect("afat:dashboard")


@login_required()
@permissions_required(
    (
        "afat.manage_afat",
        "afat.add_afatlink",
        "afat.change_afatlink",
    )
)
def link_edit(request: WSGIRequest, fatlink_hash: str = None) -> HttpResponse:
    """
    edit fatlink view
    :param request:
    :param fatlink_hash:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(request.user)

    if fatlink_hash is None:
        request.session["msg"] = ["warning", "No FAT Link hash provided."]

        return redirect("afat:dashboard")

    try:
        link = AFatLink.objects.get(hash=fatlink_hash)
    except AFatLink.DoesNotExist:
        request.session["msg"] = ["warning", "The hash provided is not valid."]

        return redirect("afat:dashboard")

    if request.method == "POST":
        fatlink_edit_form = FatLinkEditForm(request.POST)
        manual_fat_form = AFatManualFatForm(request.POST)

        if fatlink_edit_form.is_valid():
            link.fleet = fatlink_edit_form.cleaned_data["fleet"]
            link.save()
            request.session[
                "{fatlink_hash}-task-code".format(fatlink_hash=fatlink_hash)
            ] = 1
        elif manual_fat_form.is_valid():
            character_name = manual_fat_form.cleaned_data["character"]
            system = manual_fat_form.cleaned_data["system"]
            shiptype = manual_fat_form.cleaned_data["shiptype"]
            creator = request.user
            character = get_or_create_char(name=character_name)
            created_at = timezone.now()

            if character is not None:
                AFat(
                    afatlink_id=link.pk,
                    character=character,
                    system=system,
                    shiptype=shiptype,
                ).save()

                ManualAFat(
                    afatlink_id=link.pk,
                    creator=creator,
                    character=character,
                    created_at=created_at,
                ).save()

                request.session[
                    "{fatlink_hash}-task-code".format(fatlink_hash=fatlink_hash)
                ] = 3
            else:
                request.session[
                    "{fatlink_hash}-task-code".format(fatlink_hash=fatlink_hash)
                ] = 4
        else:
            request.session[
                "{fatlink_hash}-task-code".format(fatlink_hash=fatlink_hash)
            ] = 0

    msg_code = None
    message = None

    if "msg" in request.session:
        msg_code = 999
        message = request.session.pop("msg")
    elif (
        "{fatlink_hash}-creation-code".format(fatlink_hash=fatlink_hash)
        in request.session
    ):
        msg_code = request.session.pop(
            "{fatlink_hash}-creation-code".format(fatlink_hash=fatlink_hash)
        )
    elif (
        "{fatlink_hash}-task-code".format(fatlink_hash=fatlink_hash) in request.session
    ):
        msg_code = request.session.pop(
            "{fatlink_hash}-task-code".format(fatlink_hash=fatlink_hash)
        )

    # Flatlist / Raw Data Tab (deactivated as of 2020-12-26)
    # fats = AFat.objects.filter(afatlink=link)
    # flatlist = None
    # if len(fats) > 0:
    #     flatlist = []
    #
    #     for fat in fats:
    #         fatinfo = [fat.character.character_name, str(fat.system), str(fat.shiptype)]
    #         flatlist.append("\t".join(fatinfo))
    #
    #     flatlist = "\r\n".join(flatlist)

    # let's see if the link is still valid or has expired already
    link_ongoing = True
    try:
        dur = ClickAFatDuration.objects.get(fleet=link)
        now = timezone.now() - timedelta(minutes=dur.duration)

        if now >= link.afattime:
            # link expired
            link_ongoing = False
    except ClickAFatDuration.DoesNotExist:
        # ESI lnk
        link_ongoing = False

    context = {
        "form": AFatLinkForm,
        "msg_code": msg_code,
        "message": message,
        "link": link,
        # "flatlist": flatlist,
        "link_ongoing": link_ongoing,
        "permissions": permissions,
    }

    logger.info(
        "FAT link {fatlink_hash} edited by {user}".format(
            fatlink_hash=fatlink_hash, user=request.user
        )
    )

    return render(request, "afat/fleet_edit.html", context)


@login_required()
@permissions_required(
    (
        "afat.manage_afat",
        "afat.add_afatlink",
        "afat.change_afatlink",
    )
)
def link_edit_fat_data(request: WSGIRequest, fatlink_hash):
    """
    ajax call
    fat list in link edit view
    :param request:
    :param fatlink_hash:
    """

    fats = AFat.objects.filter(afatlink__hash=fatlink_hash)

    fat_rows = [convert_fats_to_dict(request=request, fat=fat) for fat in fats]

    return JsonResponse(fat_rows, safe=False)


@login_required()
@permissions_required(("afat.manage_afat", "afat.delete_afatlink"))
def del_link(request: WSGIRequest, fatlink_hash: str = None):
    """
    delete fatlink helper
    :param request:
    :param fatlink_hash:
    :return:
    """

    if fatlink_hash is None:
        request.session["msg"] = ["warning", "No FAT Link hash provided."]

        return redirect("afat:dashboard")

    try:
        link = AFatLink.objects.get(hash=fatlink_hash)
    except AFatLink.DoesNotExist:
        request.session["msg"] = [
            "danger",
            "The fatlink hash provided is either invalid or "
            "the fatlink has already been deleted.",
        ]

        return redirect("afat:dashboard")

    AFat.objects.filter(afatlink_id=link.pk).delete()

    link.delete()

    AFatDelLog(remover=request.user, deltype=0, string=link.__str__()).save()

    request.session["msg"] = [
        "success",
        "The FAT Link ({fatlink_hash}) and all associated FATs "
        "have been successfully deleted.".format(fatlink_hash=fatlink_hash),
    ]

    logger.info("FAT link %s deleted by %s", fatlink_hash, request.user)

    return redirect("afat:links")


@login_required()
@permissions_required(("afat.manage_afat", "afat.delete_afat"))
def del_fat(request: WSGIRequest, fatlink_hash: str, fat):
    """
    delete fat helper
    :param request:
    :param fatlink_hash:
    :param fat:
    :return:
    """

    try:
        link = AFatLink.objects.get(hash=fatlink_hash)
    except AFatLink.DoesNotExist:
        request.session["msg"] = [
            "danger",
            "The hash provided is either invalid or has been deleted.",
        ]

        return redirect("afat:dashboard")

    try:
        fat_details = AFat.objects.get(pk=fat, afatlink_id=link.pk)
    except AFat.DoesNotExist:
        request.session["msg"] = [
            "danger",
            "The hash and FAT ID do not match.",
        ]

        return redirect("afat:dashboard")

    fat_details.delete()
    AFatDelLog(remover=request.user, deltype=1, string=fat_details.__str__()).save()

    request.session["msg"] = [
        "success",
        "The FAT for {character_name} has been successfully "
        "deleted from link {fatlink_hash}.".format(
            character_name=fat_details.character.character_name,
            fatlink_hash=fatlink_hash,
        ),
    ]

    logger.info("FAT %s deleted by %s", fat_details, request.user)

    return redirect("afat:link_edit", fatlink_hash=fatlink_hash)
