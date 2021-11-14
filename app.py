from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Response, render_template, request
import flask_sqlalchemy, os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ktmornyueendxp:bfa6586b37549edd37ce1096c7c1563ac48f3358448981ee04dd4ee0816f4083@ec2-44-193-182-0.compute-1.amazonaws.com:5432/d9uolnhsqlmh31'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/savs_database"
db = SQLAlchemy(app)

if __name__ == '__main__':
    from application.controller.controllers import *
    app.run(debug=True, host='127.0.0.1', port=5000)