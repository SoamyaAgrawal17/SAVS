import logging
import json

from application.service import ClubService
from flask import Blueprint
from flask import request, Response

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

mod = Blueprint('club_control', __name__)


# Get a list of details of all clubs
@mod.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = ClubService.get_clubs()
    res = json.dumps(clubs, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Get details of a club specified by id
@mod.route('/clubs/<club_id>', methods=['GET'])
def get_club_by_id(club_id):
    event = ClubService.get_club(club_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Edit a club
@mod.route('/clubs/<club_id>', methods=['PUT'])
def edit_club(club_id):
    data = request.get_json()
    email_id = data["emailId"]
    if 'new_head' in data:
        head_email_id = data["new_head"]
        res, code = ClubService.assign_successor(
            email_id, club_id, head_email_id)
    else:
        club_information = data["club"]
        res, code = ClubService.edit_club(email_id, club_id, club_information)
    rsp = Response(res, status=code, content_type="text/plain")
    return rsp


# Delete a club
@mod.route('/clubs/<club_id>', methods=['DELETE'])
def delete_club(club_id):
    data = request.get_json()
    email_id = data["emailId"]
    res, code = ClubService.delete_club(email_id, club_id)
    rsp = Response(res, status=code, content_type="text/plain")
    return rsp


# Add a member to a club
@mod.route('/member/<club_id>', methods=['PUT'])
def add_member(club_id=None):
    data = request.get_json()
    email_id = data["emailId"]
    student_email_id = data["student_email_id"]
    res, code = ClubService.add_member(email_id, club_id, student_email_id)
    rsp = Response(res, status=code, content_type="application/JSON")
    return rsp


# Remove a member from a club
@mod.route('/member/<club_id>', methods=['DELETE'])
def remove_member(club_id=None):
    data = request.get_json()
    email_id = data["emailId"]
    student_email_id = data["student_email_id"]
    res, code = ClubService.remove_member(email_id, club_id, student_email_id)
    rsp = Response(res, status=code, content_type="application/JSON")
    return rsp
