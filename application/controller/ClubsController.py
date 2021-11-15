import logging
import json

from application.service import ClubService
from application.service import StudentService
from application.model.Role import Role
from flask import Blueprint
from flask import request, Response

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

mod = Blueprint('club_control', __name__)


@mod.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = ClubService.get_clubs()
    res = json.dumps(clubs, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@mod.route('/clubs/<club_id>', methods=['GET'])
def get_club_by_id(club_id):
    event = ClubService.get_club(club_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@mod.route('/clubs/<club_id>', methods=['PUT'])
def edit_club(club_id):
    data = request.get_json()
    email_id = data["emailId"]
    if email_id is None:
        return Response("Invalid Request", status=200, content_type="text/plain")
    club_information = data["club"]
    student_id = StudentService.get_id(email_id)
    if student_id is None:
        return Response("Invalid Request", status=200, content_type="text/plain")
    query = Role.query.filter_by(club_id=club_id, student_id=student_id)
    result = query.first()
    if result is None or result.role != "Club Head":
        return Response("Invalid Request", status=200, content_type="text/plain")
    res = ClubService.edit_club(club_id, club_information)
    rsp = Response(res, status=200, content_type="text/plain")
    return rsp


@mod.route('/clubs/<club_id>', methods=['DELETE'])
def delete_club(club_id):
    data = request.get_json()
    email_id = data["emailId"]
    if email_id is None:
        return Response("Invalid Request", status=200, content_type="text/plain")
    student_id = StudentService.get_id(email_id)
    if student_id is None:
        return Response("Invalid Request", status=200, content_type="text/plain")
    query = Role.query.filter_by(club_id=club_id, student_id=student_id)
    result = query.first()
    if result is None or result.role != "Club Head":
        return Response("Invalid Request", status=200, content_type="text/plain")
    res = ClubService.delete_club(club_id)
    rsp = Response(res, status=200, content_type="text/plain")
    return rsp


@mod.route('/member/<club_id>', methods=['PUT'])
def add_member(club_id=None):
    data = request.get_json()
    email_id = data["emailId"]
    student_email_id = data["student_email_id"]
    if email_id is None:
        return Response("Invalid Request", status=200, content_type="text/plain")
    editor_student_id = StudentService.get_id(email_id)
    if editor_student_id is None:
        return Response("Invalid Request", status=200, content_type="text/plain")
    student_id = StudentService.get_id(student_email_id)
    if student_id is None:
        return Response("error: student isn't registered", status=200, content_type="text/plain")
    query = Role.query.filter_by(club_id=club_id, student_id=editor_student_id)
    result = query.first()
    if result is None or result.role != "Club Head":
        return Response("Invalid Request", status=200, content_type="text/plain")
    member = ClubService.add_member(club_id, student_id)
    rsp = Response(member, status=200, content_type="application/JSON")
    return rsp
