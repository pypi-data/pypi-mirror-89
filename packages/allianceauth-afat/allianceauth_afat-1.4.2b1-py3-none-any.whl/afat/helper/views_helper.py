"""
views helper
"""

import random

from afat.models import AFat, AFatLink
from afat.permissions import get_user_permissions
from allianceauth.eveonline.models import EveCharacter
from django.urls import reverse


def convert_fatlinks_to_dict(fatlink: AFatLink, user) -> dict:
    """
    converts a AFatLink object into a dictionary
    :param fatlink:
    :param user:
    :return:
    """

    # get users permissions
    permissions = get_user_permissions(user)

    # fleet name
    fatlink_fleet = fatlink.hash

    if fatlink.fleet:
        fatlink_fleet = fatlink.fleet

    # esi marker
    via_esi = "No"
    esi_fleet_marker = ""

    if fatlink.is_esilink:
        via_esi = "Yes"
        esi_fleet_marker_classes = "label label-success afat-label afat-label-via-esi"

        if fatlink.is_registered_on_esi:
            esi_fleet_marker_classes += " afat-label-active-esi-fleet"

        esi_fleet_marker += f'<span class="{esi_fleet_marker_classes}">via ESI</span>'

    # fleet type
    fatlink_type = ""

    if fatlink.link_type:
        fatlink_type = fatlink.link_type.name

    # creator name
    creator_name = fatlink.creator.username

    if fatlink.creator.profile.main_character is not None:
        creator_name = fatlink.creator.profile.main_character.character_name

    # fleet time
    time = fatlink.afattime

    # number of FATs
    fats_number = fatlink.number_of_fats

    # action buttons
    actions = ""
    if permissions["fatlinks"]["manipulate"]:
        if permissions["fatlinks"]["change"]:
            button_edit_url = reverse("afat:link_edit", args=[fatlink.hash])

            actions += (
                '<a class="btn btn-afat-action btn-info btn-sm" href="'
                + button_edit_url
                + '">'
                '<span class="glyphicon glyphicon-pencil"></span>'
                "</a>"
            )

        if permissions["fatlinks"]["delete"]:
            button_delete_url = reverse("afat:link_delete", args=[fatlink.hash])

            actions += (
                '<a class="btn btn-afat-action btn-danger btn-sm" data-toggle="modal" '
                'data-target="#deleteModal" data-url="' + button_delete_url + '" '
                'data-name="' + fatlink_fleet + '">'
                '<span class="glyphicon glyphicon-trash"></span>'
                "</a>"
            )

    summary = {
        "pk": fatlink.pk,
        "fleet_name": fatlink_fleet + esi_fleet_marker,
        "creator_name": creator_name,
        "fleet_type": fatlink_type,
        "fleet_time": time,
        "fats_number": fats_number,
        "hash": fatlink.hash,
        "is_esilink": fatlink.is_esilink,
        "esi_fleet_id": fatlink.esi_fleet_id,
        "is_registered_on_esi": fatlink.is_registered_on_esi,
        "actions": actions,
        "via_esi": via_esi,
    }

    return summary


def convert_fats_to_dict(fat: AFat) -> dict:
    """
    converts a afat object into a dictionary
    :param fatlink:
    """

    # fleet type
    fleet_type = ""
    if fat.afatlink.link_type is not None:
        fleet_type = fat.afatlink.link_type.name

    # esi marker
    via_esi = "No"
    esi_fleet_marker = ""

    if fat.afatlink.is_esilink:
        via_esi = "Yes"
        esi_fleet_marker_classes = "label label-success afat-label afat-label-via-esi"

        if fat.afatlink.is_registered_on_esi:
            esi_fleet_marker_classes += " afat-label-active-esi-fleet"

        esi_fleet_marker += f'<span class="{esi_fleet_marker_classes}">via ESI</span>'

    summary = {
        "system": fat.system,
        "ship_type": fat.shiptype,
        "character_name": fat.character.character_name,
        "fleet_name": fat.afatlink.fleet + esi_fleet_marker,
        "fleet_time": fat.afatlink.afattime,
        "fleet_type": fleet_type,
        "via_esi": via_esi,
    }

    return summary


def convert_evecharacter_to_dict(evecharacter: EveCharacter) -> dict:
    """
    converts an EveCharacter object into a dictionary
    :param fatlink:
    """

    summary = {"character_id": "", "character_name": ""}

    return summary


def get_random_rgba_color():
    """
    get a random RGB(a) color
    :return:
    """
    return "rgba({red}, {green}, {blue}, 1)".format(
        red=random.randint(0, 255),
        green=random.randint(0, 255),
        blue=random.randint(0, 255),
    )
