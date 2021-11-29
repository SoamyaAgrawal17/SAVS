from flask import request, Response
from flask import Blueprint
import logging
import json

from application.service import EventService, StudentService


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
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Get list of filtered events
@mod.route('/filtered_events', methods=['GET'])
def get_filtered_events():
    data = request.get_json()
    filters = data["filters"]
    events = EventService.get_filtered_events(filters)
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Add an event (by club member/head)
@mod.route('/events', methods=['POST'])
def propose_events():
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")
    try:
        data = request.get_json()
        email_id = data["emailId"]
        event_information = data["event"]
        student_id = StudentService.get_id(email_id)
        response_message, status_code = EventService.propose_event(
            event_information, student_id)
        rsp = Response(response_message, status=status_code,
                       content_type="text/plain")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="text/plain")
    return rsp


# Edit an event (by club member/head)
@mod.route('/events/<event_id>', methods=['PUT'])
def edit_events(event_id):
    data = request.get_json()
    email_id = data["emailId"]
    event_information = data["event"]
    student_id = StudentService.get_id(email_id)
    response_message, status_code = EventService.edit_event(
        event_information, event_id, student_id)
    rsp = Response(response_message, status=status_code,
                   content_type="text/plain")
    return rsp

# Delete an event by club head
@mod.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    data = request.get_json()
    email_id = data["emailId"]
    student_id = StudentService.get_id(email_id)
    response_message, status_code = EventService.edit_event(event_id, student_id)
    rsp = Response(response_message, status=status_code,
                   content_type="text/plain")
    return rsp


# Get details of an event with specified id
@mod.route('/events/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    event = EventService.get_event(event_id)
    res = json.dumps(event.as_dict(), default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp
