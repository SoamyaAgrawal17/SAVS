from flask import Flask, request, jsonify, Response
from flask import Blueprint
import logging
import json

from application.service import EventService, StudentService
from application.utilities.database import db
from application.model.Role import Role


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

mod = Blueprint('events', __name__)


@mod.route('/events', methods=['GET'])
def get_events():
    events = EventService.get_events()
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@mod.route('/events', methods=['POST'])
def propose_events():
    data = request.get_json()
    email_id = data["emailId"]
    event_information = data["event"]
    club_id = data["event"]["club_id"]
    student_id = StudentService.get_id(email_id)
    query = db.session.query(Role).filter(Role.student_id.in_([student_id]))
    results = query.all()
    flag = False

    for result in results:
        if result.club_id == club_id and result.role == "Club Member":
            flag = True

    if flag == True:
        event_entry = EventService.propose_event(event_information)
    #res = json.dumps(event_entry, default=str)
    rsp = Response("CREATED", status=201, content_type="text/plain")
    return rsp


@mod.route('/events/<event_id>', methods=['PUT'])
def edit_events(event_id):
    data = request.get_json()
    email_id = data["emailId"]
    event_information = data["event"]
    club_id = data["event"]["club_id"]
    student_id = StudentService.get_id(email_id)
    query = db.session.query(Role).filter(Role.student_id.in_([student_id]))
    results = query.all()
    flag = False

    for result in results:
        if result.club_id == club_id and result.role == "Club Member":
            flag = True

    if flag == True:
        event_entry = EventService.edit_event(event_information, event_id)
    #res = json.dumps(event_entry, default=str)
    rsp = Response("CREATED", status=201, content_type="text/plain")
    return rsp


@mod.route('/events/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    event = EventService.get_event(event_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@mod.route('/events/<event_id>', methods=['PUT'])
def edit_event(event_id):
    event = EventService.edit_event(event_id)
    rsp = Response("OK", status=200, content_type="text/plain")
    return rsp


@mod.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    rsp = Response("OK", status=200, content_type="text/plain")
    return rsp