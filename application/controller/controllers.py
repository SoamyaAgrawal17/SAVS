from flask import Flask, request, jsonify, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy
from application.service import EventService
import logging
import json

from application.service import EventService, ClubService

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ktmornyueendxp:bfa6586b37549edd37ce1096c7c1563ac48f3358448981ee04dd4ee0816f4083@ec2-44-193-182-0.compute-1.amazonaws.com:5432/d9uolnhsqlmh31'
db = SQLAlchemy(app)

@app.route('/events', methods=['GET'])
def get_events():
    events = EventService.get_events()
    res = json.dumps(events, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@app.route('/events', methods=['POST'])
def add_events():
    rsp = Response("CREATED", status=201, content_type="text/plain")
    return rsp


@app.route('/events/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    event = EventService.get_event(event_id)
    res = json.dumps(event, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return rsp


@app.route('/events/<event_id>', methods=['PUT'])
def edit_event(event_id):
    event = EventService.edit_event(event_id)
    rsp = Response("OK", status=200, content_type="text/plain")
    return rsp


@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    rsp = Response("OK", status=200, content_type="text/plain")
    return rsp

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