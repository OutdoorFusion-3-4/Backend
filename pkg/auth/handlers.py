from flask import request
import jwt
from pkg.server.server import api, app
import pkg.auth.authentication as authentication
from flask import request, make_response, Response

import datetime


@api.before_request
def validateToken():
    if request.path == '/api/login' or request.path == '/api/register':
        return

    token = request.cookies.get('Token')
    if token is None:
        return Response('Unauthorized', status=401)

    try:
        jwt.decode(token, app.config["SECRET_KEY"])
    except:
        return Response('Unauthorized', status=401)

@api.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    resp = make_response()

    if authentication.Login(username=username, password=password):
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config[
            "SECRET_KEY"])

        resp.set_cookie("Token", token, httponly=True)
        resp.set_cookie("Authenticated", "", httponly=False)
        return resp

    return Response('Invalid username or password', status=401)


@api.route('/register', methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if authentication.register(username=username, password=password):
        return Response("User successfully created", status=200)

    return Response(response="Username already exists", status=409)


@api.route('/logout', methods=["POST"])
def logout():
    resp = make_response()

    resp.delete_cookie("Token")
    resp.delete_cookie("Authenticated")

    return resp

