from flask import Flask, request, jsonify, Response
import logging
import json

from application.service import EventService

from controllers import app

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


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