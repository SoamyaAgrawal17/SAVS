from flask import Flask, request, jsonify, Response
import logging
import json

from app.service import EventService, ClubService

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)