from flask import Flask, request, jsonify, Response
import logging
import json

from controllers import app
from application.service import ClubService

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = ClubService.get_clubs()
    res = json.dumps(clubs, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@app.route('/clubs', methods=['POST'])
def add_clubs():
    rsp = Response("CREATED", status=201, content_type="text/plain")
    return rsp


@app.route('/clubs/<club_id>', methods=['GET'])
def get_club_by_id(club_id):
    event = ClubService.get_event(club_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@app.route('/clubs/<club_id>', methods=['PUT'])
def edit_club(club_id):
    event = ClubService.edit_event(club_id)
    rsp = Response("OK", status=200, content_type="text/plain")
    return rsp


@app.route('/clubs/<club_id>', methods=['DELETE'])
def delete_club(club_id):
    rsp = Response("OK", status=200, content_type="text/plain")
    return rsp
