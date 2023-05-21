import csv
import datetime
import os

import jwt
from flask import Flask, request, make_response, Response
from ..fileUpload import fileUpload
from core.ml import predictor
from src.cmd.api import Authentication


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = str(os.getenv("JWT_TOKEN"))

        @self.app.route('/api/predictions', methods=['GET'])
        def predict():
            dates = request.args.get('dates')
            logs = request.args.get('logs')
            predictionType: predictor.PredictableValues = request.args.get('predictionType')

            p = predictor.Predictor().loadModel(predictionType)

            return p.Predict(dates, logs=logs)

        @self.app.route('/api/login', methods=['POST'])
        def login():
            username = request.form.get('username')
            password = request.form.get('password')

            resp = make_response()

            if Authentication.authentication.Login(self, username=username, password=password):
                token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, self.app.config[
                    "SECRET_KEY"])

                resp.set_cookie("Token", token, httponly=True)
                resp.set_cookie("Authenticated", "", httponly=True)
                return resp

            return Response('Invalid username or password', status=401)

        @self.app.route('/api/register', methods=["POST"])
        def register():
            username = request.form.get('username')
            password = request.form.get('password')

            if Authentication.authentication.register(self, username=username, password=password):
                return Response("User succesfully created", status=200)

            return Response(response="Username already exists", status=409)

        @self.app.route('/api/logout', methods=["POST"])
        def logout():
            resp = make_response()

            resp.delete_cookie("Token")
            resp.delete_cookie("Authenticated")

            return resp

        @self.app.route('/api/upload', methods=['POST'])
        def uploadFiles():
            fileType: fileUpload.FileTypes = request.args.get('fileType')
            file = request.files['file']
            if file is None:
                return "400"

            fileUpload.UploadFile(file, fileType).parseCSV()
            return "200"

    def run(self):

        # port veranderd naar 80 omdat andere port het niet deed.
        port = int(os.getenv('PORT', 80))
        self.app.run(port=port)
