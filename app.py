from flask_sqlalchemy import SQLAlchemy
from application.utilities.database import db
from flask import Flask, request, jsonify, Response, render_template, request
import flask_sqlalchemy, os
from application.controller import ClubsController, EventsController, StudentsController
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ktmornyueendxp:bfa6586b37549edd37ce1096c7c1563ac48f3358448981ee04dd4ee0816f4083@ec2-44-193-182-0.compute-1.amazonaws.com:5432/d9uolnhsqlmh31'


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