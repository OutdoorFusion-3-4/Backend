
import csv
import datetime
import os

import jwt
from flask import Flask, request, make_response, Response, Blueprint
from ..fileUpload import fileUpload
from core.ml import predictor
from src.cmd.api import Authentication
from pkg.queries.DataQueries import DataQueries
from pkg.queries.types import GraphQueryParameters


@app.route('/api/predictions', methods=['GET'])
def predict():
    dates = request.args.get('dates')
    logs = request.args.get('logs')
    predictionType: predictor.PredictableValues = request.args.get('predictionType')

    p = predictor.Predictor().loadModel(predictionType)

    return p.Predict(dates, logs=logs)


@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    resp = make_response()

    if Authentication.Login(username=username, password=password):
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config[
            "SECRET_KEY"])

        resp.set_cookie("Token", token, httponly=False)
        resp.set_cookie("Authenticated", "", httponly=False)
        return resp

    return Response('Invalid username or password', status=401)


@app.route('/api/register', methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if Authentication.register(username=username, password=password):
        return Response("User succesfully created", status=200)

    return Response(response="Username already exists", status=409)


@app.route('/api/logout', methods=["POST"])
def logout():
    resp = make_response()

    resp.delete_cookie("Token")
    resp.delete_cookie("Authenticated")

    return resp


@app.route('/api/upload', methods=['POST'])
def uploadFiles():
    fileType: fileUpload.FileTypes = request.args.get('fileType')
    file = request.files['file']
    if file is None:
        return "400"

    fileUpload.UploadFile(file, fileType).parseCSV()
    return "200"


def run():
    # port veranderd naar 80 omdat andere port het niet deed.
    port = int(os.getenv('PORT', 80))
    app.run(port=port)

db = Database()
port = int(os.getenv('PORT', 8080))

api = Blueprint('api_routes', __name__,
                template_folder='api')



def getGraphQueryParameters() -> GraphQueryParameters:
    params = GraphQueryParameters()
    params.dateStart = request.args.get('dateStart')
    params.dateEnd = request.args.get('dateEnd')
    params.companies = request.args.get('companies')
    return params


@api.route('/predictions', methods=['GET'])
def predict():
    dates = request.args.get('dates')
    logs = request.args.get('logs')
    predictionType: predictor.PredictableValues = request.args.get(
        'predictionType')

    p = predictor.Predictor().loadModel(predictionType)

    return p.Predict(dates, logs=logs)


@api.route('/login', methods=['POST'])
def login():
    """Logic for login endpoint"""


@api.route('/upload', methods=['POST'])
def uploadFiles():
    fileType: fileUpload.FileTypes = request.args.get('fileType')
    file = request.files['file']
    if file is None:
        return "400"

    """Logic for file upload"""

    return "200"


@api.route('/revenues', methods=['GET'])
def revenues():
    params = getGraphQueryParameters()
    return jsonify(DataQueries(db, params).Revenues())


@api.route('/profits', methods=['GET'])
def profits():
    params = getGraphQueryParameters()
    return jsonify(DataQueries(db, params).Profits())


@api.route('/orders', methods=['GET'])
def orders():
    params = getGraphQueryParameters()
    return jsonify(DataQueries(db, params).Orders())


@api.route('/categories', methods=['GET'])
def categories():
    params = getGraphQueryParameters()
    return DataQueries(db, params).Categories()


@api.route('/order-methods', methods=['GET'])
def orderMethods():
    params = getGraphQueryParameters()
    return DataQueries(db, params).OrderMethods()


@api.route('/products', methods=['GET'])
def products():
    params = getGraphQueryParameters()
    return DataQueries(db, params).Products()


@api.route('/countries', methods=['GET'])
def countries():
    params = getGraphQueryParameters()
    return DataQueries(db, params).Countries()

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.config['SECRET_KEY'] = str(os.getenv("JWT_TOKEN"))

def run():
    app.run(port=port, debug=True)
