from flask import request, jsonify, Response, render_template, request
import logging
import json, sys
from app import app

from application.service import EventService, ClubService, StudentService

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# TODO @Vani and @Soamya
# Signup a student
@app.route('/student', methods=['POST'])
def create_student():

    student_information = request.get_json()
    student_entry = StudentService.create_student_db(student_information)
    res = json.dumps(student_entry, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp

#TODO @Vani and @Soamya
#Signup a student
@app.route('/student/<email_id>', methods=['GET'])
def get_student(email_id=None):
    
    student_entry = StudentService.get_student_db(email_id)
    res = json.dumps(student_entry, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp

#TODO @Vani and @Soamya
#View all upcoming events.
@app.route('/events', methods=['GET'])
def get_events():
    events = EventService.get_events()
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp

# #TODO @Vani and @Soamya
# #View details of a particular event. 
# @app.route('/events/<event_id>/student/<student_id>', methods=['GET'])
# def get_event_by_id(event_id):
#     event = EventService.get_event(event_id)
#     res = json.dumps(event, default=str)
#     rsp = Response(res, status=200, content_type="application/JSON")
#     return rsp


# #TODO @Vani and @Soamya
# #Register for an event
# @app.route('/events/<event_id>/student/<student_id>', methods=['GET'])
# def get_event_by_id(event_id):
#     event = EventService.get_event(event_id)
#     res = json.dumps(event, default=str)
#     rsp = Response(res, status=200, content_type="application/JSON")
#     return rsp

# #TODO @Vani and @Soamya
# #View my registered events
# @app.route('/student/<student_id>', methods=['GET'])
# def get_event_by_id(event_id):
#     event = StudentService.get_registered_events(event_id)
#     res = json.dumps(event, default=str)
#     rsp = Response(res, status=200, content_type="application/JSON")
#     return rsp

# #TODO @Vani and @Soamya
# #Create a new club
# @app.route('/clubs/student/<student_id>', methods=['POST'])
# def add_clubs():
#     rsp = Response("CREATED", status=201, content_type="text/plain")
#     return rsp

# #TODO @Vani and @Soamya
# #View all the clubs and my role in it
# @app.route('/clubs/student/<student_id>', methods=['POST'])
# def add_clubs():
#     rsp = Response("CREATED", status=201, content_type="text/plain")
#     return rsp


# @app.route('/events', methods=['POST'])
# def add_events():
#     rsp = Response("CREATED", status=201, content_type="text/plain")
#     return rsp


# @app.route('/events/<event_id>', methods=['PUT'])
# def edit_event(event_id):
#     event = EventService.edit_event(event_id)
#     rsp = Response("OK", status=200, content_type="text/plain")
#     return rsp


# @app.route('/events/<event_id>', methods=['DELETE'])
# def delete_event(event_id):
#     rsp = Response("OK", status=200, content_type="text/plain")
#     return rsp

# @app.route('/clubs', methods=['GET'])
# def get_clubs():
#     clubs = ClubService.get_clubs()
#     res = json.dumps(clubs, default=str)
#     rsp = Response(res, status=200, content_type="application/JSON")
#     return rsp





# @app.route('/clubs/<club_id>', methods=['GET'])
# def get_club_by_id(club_id):
#     event = ClubService.get_event(club_id)
#     res = json.dumps(event, default=str)
#     rsp = Response(res, status=200, content_type="application/JSON")
#     return rsp


# @app.route('/clubs/<club_id>', methods=['PUT'])
# def edit_club(club_id):
#     event = ClubService.edit_event(club_id)
#     rsp = Response("OK", status=200, content_type="text/plain")
#     return rsp


# @app.route('/clubs/<club_id>', methods=['DELETE'])
# def delete_club(club_id):
#     rsp = Response("OK", status=200, content_type="text/plain")
#     return rsp


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)