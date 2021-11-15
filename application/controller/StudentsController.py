import logging
import json
from flask import Blueprint, request, Response
from application.service import EventService, ClubService, StudentService

mod = Blueprint('students', __name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# Signup a student
@mod.route('/student', methods=['POST'])
def create_student():
    student_information = request.get_json()
    student_entry = StudentService.create_student(student_information)
    res = json.dumps(student_entry, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Get student information
@mod.route('/student/<email_id>', methods=['GET'])
def get_student(email_id=None):
    student_entry = StudentService.get_student(email_id)
    res = json.dumps(student_entry, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# View all upcoming events.
@mod.route('/student/<student_email_id>/get_upcoming_events', methods=['GET'])
def get_upcoming_events(student_email_id=None):
    events = EventService.get_upcoming_events(student_email_id)
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# View details of a particular event.
@mod.route('/student/<student_id>/get_event/<event_id>', methods=['GET'])
def get_event_by_id(event_id=None, student_id=None):
    event = EventService.get_event(event_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Register for an event
@mod.route('/student/<student_id>/register_event/<event_id>', methods=['GET'])
def register_event(event_id=None, student_id=None):
    event = EventService.register_event(event_id, student_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# View registered events
@mod.route('/student/<student_id>/get_registered_events', methods=['GET'])
def get_registered_events(student_id):
    event = EventService.get_registered_events(student_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Create a new club
@mod.route('/student/<student_email_id>/club', methods=['POST'])
def create_club(student_email_id=None):
    club_information = request.get_json()
    status, club_entry = ClubService.create_club(club_information)
    res = json.dumps(club_entry, default=str)
    rsp = Response(res, status=status, content_type="application/JSON")
    return rsp


# View all the clubs and my role in it
@mod.route('/student/<student_id>/get_roles', methods=['GET'])
def get_roles(student_id=None):
    clubs = ClubService.get_roles(student_id)
    res = json.dumps(clubs, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp

