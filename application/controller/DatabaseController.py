import logging
import json
from flask import Blueprint, Response
from application.service import DatabaseService

mod = Blueprint('database', __name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@mod.route('/database/clear_database', methods=['GET'])
def clear_database():
    try:
        status = DatabaseService.clear_database()
        res = json.dumps(status, default=str)
        rsp = Response(res, status=200, content_type="application/JSON")
    except Exception as e:
        print("/api/<resource>, e = ", e)
        rsp = Response(e, status=500, content_type="plain/text")
    return rsp


