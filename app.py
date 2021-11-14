from flask_sqlalchemy import SQLAlchemy
from application.utilities.database import db
from flask import Flask, request, jsonify, Response, render_template, request
import flask_sqlalchemy, os
from application.controller import ClubsController, EventsController, StudentsController
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uoaidyfadwrwpe:72aae551e395c9450d8611d0e0dc52856ca98b4e9b22b4cbada9b4bb894d653c@ec2-23-23-133-10.compute-1.amazonaws.com:5432/d1e9sornll6622'


blueprints = [
    ClubsController.mod,
    StudentsController.mod,
    EventsController.mod
]

for bp in blueprints:
    app.register_blueprint(bp)

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)