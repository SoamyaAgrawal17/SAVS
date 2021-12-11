from flask import request, Response
from flask import Blueprint
import logging
import json

from application.auth.google_auth import auth_required, get_token_info
from application.service import EventService, StudentService
from application.utilities.constants import CONTENT_TYPE_JSON,\
    CONTENT_TYPE_TEXT, API_ERROR

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

mod = Blueprint('events', __name__)


# Get list of all events
# If created_by is send as part of query params
# Return list of events created_by the student (club member)
@mod.route('/events', methods=['GET'])
def get_events():
    created_by = request.args.get('created_by')
    events_list = EventService.get_events(created_by)
    events = [event.as_dict() for event in events_list]
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type=CONTENT_TYPE_JSON)
    return rsp


# Get list of filtered events
@mod.route('/filtered_events', methods=['GET'])
def get_filtered_events():
    data = request.get_json()
    filters = data["filters"]
    events = EventService.get_filtered_events(filters)
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type=CONTENT_TYPE_JSON)
    return rsp


# Add an event (by club member/head)
@mod.route('/events', methods=['POST'])
@auth_required
def propose_events():
    rsp = Response("INTERNAL ERROR", status=500,
                   content_type=CONTENT_TYPE_TEXT)
    try:
        data = request.get_json()
        user_info = get_token_info()
        email_id = user_info["email"]
        event_information = data["event"]
        student_id = StudentService.get_id(email_id)
        response_message, status_code = EventService.propose_event(
            event_information, student_id)
        rsp = Response(response_message, status=status_code,
                       content_type=CONTENT_TYPE_TEXT)
    except Exception as e:
        print(API_ERROR, e)
        rsp = Response(e, status=500, content_type=CONTENT_TYPE_TEXT)
    return rsp


# Edit an event (by club member/head)
@mod.route('/events/<event_id>', methods=['PUT'])
@auth_required
def edit_events(event_id):
    rsp = Response("INTERNAL ERROR", status=500,
                   content_type=CONTENT_TYPE_TEXT)
    try:
        data = request.get_json()
        user_info = get_token_info()
        email_id = user_info["email"]
        if 'status' in data:
            event_status = data["status"]
            student_id = StudentService.get_id(email_id)
            response_message, status_code = EventService.decide_event_status(
                event_status, event_id, student_id)
        else:
            event_information = data["event"]
            student_id = StudentService.get_id(email_id)
            response_message, status_code = EventService.edit_event(
                event_information, event_id, student_id)
        rsp = Response(response_message, status=status_code,
                       content_type=CONTENT_TYPE_TEXT)
    except Exception as e:
        print(API_ERROR, e)
        rsp = Response(e, status=500, content_type=CONTENT_TYPE_TEXT)
    return rsp


# Delete an event by club head
@mod.route('/events/<event_id>', methods=['DELETE'])
@auth_required
def delete_event(event_id):
    user_info = get_token_info()
    email_id = user_info["email"]
    student_id = StudentService.get_id(email_id)
    response_message, status_code = EventService.delete_event(
        event_id, student_id)
    rsp = Response(response_message, status=status_code,
                   content_type=CONTENT_TYPE_TEXT)
    return rsp


# Get details of an event with specified id
@mod.route('/events/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    rsp = Response("INTERNAL ERROR", status=500,
                   content_type=CONTENT_TYPE_TEXT)
    try:
        event = EventService.get_event(event_id)
        res = json.dumps(event.as_dict(), default=str)
        rsp = Response(res, status=200, content_type=CONTENT_TYPE_JSON)
    except Exception as e:
        print(API_ERROR, e)
        rsp = Response(e, status=500, content_type=CONTENT_TYPE_TEXT)
    return rsp


@mod.route('/test', methods=['GET'])
@auth_required
def get_auth_test():
    rsp = Response("INTERNAL ERROR", status=500,
                   content_type=CONTENT_TYPE_TEXT)
    try:
        user_info = get_token_info()
        obj = {"key": user_info["email"]}
        res = json.dumps(obj, default=str)
        rsp = Response(res, status=200, content_type=CONTENT_TYPE_JSON)
    except Exception as e:
        print(API_ERROR, e)
        rsp = Response(e, status=500, content_type=CONTENT_TYPE_TEXT)
    return rsp
