import logging
import json
from flask import Blueprint, request, Response
from application.service import StudentService

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
@mod.route('/student/get_upcoming_events', methods=['GET'])
def get_upcoming_events():
    data = request.get_json()
    email_id = data["emailId"]
    events = StudentService.get_upcoming_events(email_id)
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Register for an event
@mod.route('/student/register_event/<event_id>', methods=['POST'])
def register_event(event_id=None):
    data = request.get_json()
    email_id = data["emailId"]
    student_id = StudentService.get_id(email_id)
    event = StudentService.register_event(event_id, student_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# View registered events
@mod.route('/student/get_registered_events', methods=['GET'])
def get_registered_events():
    data = request.get_json()
    email_id = data["emailId"]
    student_id = StudentService.get_id(email_id)
    event = StudentService.get_registered_events(student_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


# Create a new club
@mod.route('/student/club', methods=['POST'])
def create_club():
    data = request.get_json()
    email_id = data["emailId"]
    club_information = data["club"]
    status, club_entry = StudentService.create_club(club_information)
    res = json.dumps(club_entry, default=str)
    rsp = Response(res, status=status, content_type="application/JSON")
    return rsp


# View all the clubs and my role in it
@mod.route('/student/get_roles', methods=['GET'])
def get_roles(student_id=None):
    data = request.get_json()
    email_id = data["emailId"]
    student_id = StudentService.get_id(email_id)
    clubs = StudentService.get_roles(student_id)
    res = json.dumps(clubs, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp

