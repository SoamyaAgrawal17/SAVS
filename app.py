from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Response, render_template, request
import flask_sqlalchemy, os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xemmxmxrzwwqml:7a22441f69138467943cd7212dd0186ce219bc424589ebdf9eef8fbe08ea4af3@ec2-44-194-225-27.compute-1.amazonaws.com:5432/d76kto02mv7hb3'
db = SQLAlchemy(app)

if __name__ == '__main__':
    from application.controller.controllers import *
    app.run(debug=True, host='127.0.0.1', port=5000)