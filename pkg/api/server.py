from flask import Blueprint, Flask, request, jsonify
from core.ml import predictor
from pkg.queries.DataQueries import DataQueries
from pkg.queries.types import GraphQueryParameters
from ..fileUpload import fileUpload
from ..storage.database import Database
import os

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

def run():
    app.run(port=port, debug=True)
