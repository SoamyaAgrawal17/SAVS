from flask import Blueprint
from flask import request, Response
import logging
import json
from application.service import ClubService

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

mod = Blueprint('club_control', __name__)


@mod.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = ClubService.get_clubs()
    res = json.dumps(clubs, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@mod.route('/clubs', methods=['POST'])
def add_clubs():
    rsp = Response("CREATED", status=201, content_type="text/plain")
    return rsp


@mod.route('/clubs/<club_id>', methods=['GET'])
def get_club_by_id(club_id):
    event = ClubService.get_club(club_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@mod.route('/clubs/<club_id>', methods=['PUT'])
def edit_club(club_id):
    inputs = request.args
    res = ClubService.edit_club(club_id, inputs)
    rsp = Response(res, status=200, content_type="text/plain")
    return rsp


@mod.route('/clubs/<club_id>', methods=['DELETE'])
def delete_club(club_id):
    res = ClubService.delete_club(club_id)
    rsp = Response(res, status=200, content_type="text/plain")
    return rsp
