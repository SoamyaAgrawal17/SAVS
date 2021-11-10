from flask import Flask, request, jsonify, Response
import logging
import json

from application.service import EventService, ClubService

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)