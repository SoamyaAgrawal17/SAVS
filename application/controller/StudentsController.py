import logging
import json
from flask import Blueprint
from flask import Response, request
from application.service import EventService, ClubService, StudentService

mod = Blueprint('students', __name__)
# from app import app


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# @Vani and @Soamya
# Signup a student
@mod.route('/student', methods=['POST'])
def create_student():
    student_information = request.get_json()
    student_entry = StudentService.create_student_db(student_information)
    res = json.dumps(student_entry, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# @Vani and @Soamya
# Get student information
@mod.route('/student/<email_id>', methods=['GET'])
def get_student(email_id=None):
    student_entry = StudentService.get_student_db(email_id)
    res = json.dumps(student_entry, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# TODO @Vani and @Soamya
# View all upcoming events.
@mod.route('/get_upcoming_events/<student_email_id>', methods=['GET'])
def get_upcoming_events(student_email_id=None):
    events = EventService.get_upcoming_events(student_email_id)
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# TODO @Vani and @Soamya
# View details of a particular event.
@mod.route('/get_event/<event_id>/student/<student_id>', methods=['GET'])
def get_event_by_id(event_id=None, student_id=None):
    event = EventService.get_event(event_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# @Vani and @Soamya
# Create an event
@mod.route('/create_event', methods=['POST'])
def create_event():
    event_information = request.get_json()
    event_entry = EventService.create_event(event_information)
    res = json.dumps(event_entry, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# @Vani and @Soamya
# #Register for an event
@mod.route('/register_for_event/<event_id>/student/<student_id>',
           methods=['GET'])
def register_event(event_id=None, student_id=None):
    event = EventService.register_event(event_id, student_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# @Vani and @Soamya
# #View my registered events
@mod.route('/get_registered_events/student/<student_id>', methods=['GET'])
def get_registered_events(student_id):
    event = EventService.get_registered_events(student_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# @Vani and @Soamya
# #Create a new club
@mod.route('/clubs/student/<student_email_id>', methods=['POST'])
def add_clubs(student_email_id=None):
    club_information = request.get_json()
    club_entry = ClubService.create_club(club_information)
    res = json.dumps(club_entry, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# @Vani and @Soamya
# #View all the clubs and my role in it
@mod.route('/get_all_clubs/student/<student_id>', methods=['GET'])
def get_all_clubs(student_id=None):
    clubs = ClubService.get_all_clubs(student_id)
    res = json.dumps(clubs, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@mod.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = ClubService.get_clubs()
    res = json.dumps(clubs, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp

# if __name__ == '__main__':
#     # mod.run(debug=True, host='127.0.0.1', port=5000)
