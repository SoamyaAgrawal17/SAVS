from flask import request, Response
import requests

from application.auth.auth_error import AuthError

TOKEN_URL = "https://oauth2.googleapis.com/tokeninfo"

'''
Th function skeleton was adapted from
https://auth0.com/blog/developing-restful-apis-with-python-
and-flask/#Securing-Python-APIs-with-Auth0
'''


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError("Authorization Header Missing", 401)
    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError("Invalid Header",
                        401)
    elif len(parts) == 1:
        raise AuthError("Invalid Header: Token not found",
                        401)
    elif len(parts) > 2:
        raise AuthError("Header must be a Bearer token", 401)
    token = parts[1]
    return token


def auth_required(f):
    def decorated(*args, **kwargs):
        try:
            token_info = get_token_info()
            if 'error' in token_info.keys():
                return Response("Unauthorized", status=401, content_type="application/json")
            return f(*args, **kwargs)
        except AuthError as e:
            return Response(e.message, status=e.status, content_type="application/json")
    decorated.__name__ = f.__name__
    return decorated


def get_token_info():
    token = get_token_auth_header()
    response = requests.get(TOKEN_URL, params={'access_token': token})
    token_info = response.json()
    return token_info
