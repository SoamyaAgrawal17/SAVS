import logging
import json

from application.service import ClubService
from flask import Blueprint
from flask import request, Response
from application.auth.google_auth import auth_required, get_token_info

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Variable declaration
application_json = "application/JSON"
api_resource = "/api/<resource>, e = "
plain_text = "plain/text"

mod = Blueprint('club_control', __name__)


# Get a list of details of all clubs
@mod.route('/clubs', methods=['GET'])
def get_clubs():
    try:
        clubs = ClubService.get_clubs()
        res = json.dumps(clubs, default=str)
        rsp = Response(res, status=200, content_type=application_json)
    except Exception as e:
        print(api_resource, e)
        rsp = Response(e, status=500, content_type=plain_text)
    return rsp


# Get details of a club specified by id
@mod.route('/clubs/<club_id>', methods=['GET'])
def get_club_by_id(club_id):
    try:
        event = ClubService.get_club(club_id)
        res = json.dumps(event, default=str)
        rsp = Response(res, status=200, content_type=application_json)
    except Exception as e:
        print(api_resource, e)
        rsp = Response(e, status=500, content_type=plain_text)
    return rsp


# Edit a club
@mod.route('/clubs/<club_id>', methods=['PUT'])
@auth_required
def edit_club(club_id):
    try:
        data = request.get_json()
        user_info = get_token_info()
        email_id = user_info["email"]
        if 'new_head' in data:
            head_email_id = data["new_head"]
            res, code = ClubService.assign_successor(
                email_id, club_id, head_email_id)
        else:
            club_information = data["club"]
            res, code = ClubService.edit_club(email_id, club_id,
                                              club_information)
        rsp = Response(res, status=code, content_type="text/plain")
    except Exception as e:
        print(api_resource, e)
        rsp = Response(e, status=500, content_type=plain_text)
    return rsp


# Delete a club
@mod.route('/clubs/<club_id>', methods=['DELETE'])
@auth_required
def delete_club(club_id):
    try:
        user_info = get_token_info()
        email_id = user_info["email"]
        res, code = ClubService.delete_club(email_id, club_id)
        rsp = Response(res, status=code, content_type="text/plain")
    except Exception as e:
        print(api_resource, e)
        rsp = Response(e, status=500, content_type=plain_text)
    return rsp


# Add a member to a club
@mod.route('/member/<club_id>', methods=['PUT'])
@auth_required
def add_member(club_id=None):
    try:
        data = request.get_json()
        user_info = get_token_info()
        email_id = user_info["email"]
        student_email_id = data["student_email_id"]
        res, code = ClubService.add_member(email_id, club_id, student_email_id)
        rsp = Response(res, status=code, content_type=application_json)
    except Exception as e:
        print(api_resource, e)
        rsp = Response(e, status=500, content_type=plain_text)
    return rsp


# Remove a member from a club
@mod.route('/member/<club_id>', methods=['DELETE'])
@auth_required
def remove_member(club_id=None):
    try:
        data = request.get_json()
        user_info = get_token_info()
        email_id = user_info["email"]
        student_email_id = data["student_email_id"]
        res, code = ClubService.remove_member(email_id, club_id,
                                              student_email_id)
        rsp = Response(res, status=code, content_type=application_json)
    except Exception as e:
        print(api_resource, e)
        rsp = Response(e, status=500, content_type=plain_text)
    return rsp
