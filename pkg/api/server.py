from flask import Blueprint, Flask, request
from core.ml import predictor
from pkg.queries.DataQueries import DataQueries
from pkg.queries.types import GraphQueryParameters
from ..fileUpload import fileUpload
from ..storage.database import Database
import os

api = Blueprint('api_routes', __name__,
                template_folder='api')


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(api, url_prefix='/api')
        self.db = Database()

        def getGraphQueryParameters() -> GraphQueryParameters:
            params = GraphQueryParameters
            params.dateStart = request.args.get('dateStart')
            params.dateEnd = request.args.get('dateEnd')
            params.company = request.args.get('company')
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
        def revenues(self):
            params = getGraphQueryParameters()
            return DataQueries(self.db, params).Revenues()
        
        @api.route('/profits', methods=['GET'])
        def profits():
            params = getGraphQueryParameters()
            return DataQueries(self.db, params).Profits()
        
        @api.route('/orders', methods=['GET'])
        def orders():
            params = getGraphQueryParameters()
            return DataQueries(self.db, params).Orders()
        
        @api.route('/categories', methods=['GET'])
        def categories():
            params = getGraphQueryParameters()
            return DataQueries(self.db, params).Categories()
        
        @api.route('/order-methods', methods=['GET'])
        def orderMethods():
            params = getGraphQueryParameters()
            return DataQueries(self.db, params).OrderMethods()
        def products():
            params = getGraphQueryParameters()
            return DataQueries(self.db, params).Products()
        def countries():
            params = getGraphQueryParameters()
            return DataQueries(self.db, params).Countries()
        

    def run(self):
        port = int(os.getenv('PORT', 8080))
        self.app.run(port=port)
