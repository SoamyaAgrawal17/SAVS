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
    try:
        student_information = request.get_json()
        student_entry = StudentService.create_student(student_information)
        res = json.dumps(student_entry, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


# Get student information
@mod.route('/student/<email_id>', methods=['GET'])
def get_student(email_id=None):
    try:
        student_entry = StudentService.get_student(email_id)
        if student_entry is None:
            return "Student is not registered"
        res = json.dumps(student_entry, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


# View all upcoming events.
@mod.route('/student/get_upcoming_events', methods=['GET'])
def get_upcoming_events():
    try:
        data = request.get_json()
        email_id = data["emailId"]
        have_permission, rsp = validate_permission(email_id)
        if not have_permission:
            return rsp
        events = StudentService.get_upcoming_events(email_id)
        res = json.dumps(events, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


# Register for an event
@mod.route('/student/register_event/<event_id>', methods=['POST'])
def register_event(event_id=None):
    try:
        data = request.get_json()
        email_id = data["emailId"]
        student_id = StudentService.get_id(email_id)
        have_permission, rsp = validate_permission(student_id)
        if not have_permission:
            return rsp
        event = StudentService.register_event(event_id, student_id)
        res = json.dumps(event, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


# View registered events
@mod.route('/student/get_registered_events', methods=['GET'])
def get_registered_events():
    try:
        data = request.get_json()
        email_id = data["emailId"]
        student_id = StudentService.get_id(email_id)
        have_permission, rsp = validate_permission(student_id)
        if not have_permission:
            return rsp
        event = StudentService.get_registered_events(student_id)
        res = json.dumps(event, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


# Withdraw event
@mod.route('/student/withdraw_event', methods=['POST'])
def withdraw_event():
    try:
        data = request.get_json()
        email_id = data["emailId"]
        event_id = data["eventId"]
        student_id = StudentService.get_id(email_id)
        have_permission, rsp = validate_permission(student_id)
        if not have_permission:
            return rsp
        event = StudentService.withdraw_event(student_id, event_id)
        res = json.dumps(event, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


# Create a new club
@mod.route('/student/club', methods=['POST'])
def create_club():
    try:
        data = request.get_json()
        email_id = data["emailId"]
        student_id = StudentService.get_id(email_id)
        have_permission, rsp = validate_permission(student_id)
        if not have_permission:
            return rsp
        club_information = data["club"]
        status, club_entry = StudentService.create_club(club_information)
        res = json.dumps(club_entry, default=str)
        rsp = Response(res, status=status, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


# View all the clubs and my role in it
@mod.route('/student/get_roles', methods=['GET'])
def get_roles():
    try:
        data = request.get_json()
        email_id = data["emailId"]
        student_id = StudentService.get_id(email_id)
        have_permission, rsp = validate_permission(student_id)
        if not have_permission:
            return rsp
        clubs = StudentService.get_roles(student_id)
        res = json.dumps(clubs, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp

@mod.route('/student/cleae_database', methods=['GET'])
def clear_database():
    try:
        status = StudentService.clear_database()
        res = json.dumps(status, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


def validate_permission(student_id):
    if student_id == "Student does not exist":
        message = "You do not have the required" \
                  " permissions to perform this operation"
        return False, Response(message, status=403, content_type="plain/text")
    return True, Response("Valid student", status=200, content_type="plain/text")
