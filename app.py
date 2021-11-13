from application.controller.controllers import app
from application.controller.controllers import db

from application.model.Club import Club
from application.model.Event import Event
from application.model.Role import Role
from application.model.StudentEvent import StudentEvent
from application.model.Student import Student
from application.service import EventService, ClubService
from flask import Flask, request, jsonify, Response, render_template, request

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

@app.route('/clubs/<club_id>', methods=['PUT'])
def edit_club(club_id):
    inputs = request.args
    res = ClubService.edit_club(db, club_id, inputs)
    rsp = Response("OK", status=200, content_type="text/plain")
    return rsp