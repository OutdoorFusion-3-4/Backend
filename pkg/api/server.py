from flask import Flask, request
from core.ml import predictor
from ..fileUpload import fileUpload
import os

class Server:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/api/predictions', methods=['GET'])
        def predict():
            dates = request.args.get('dates')
            logs = request.args.get('logs')
            predictionType: predictor.PredictableValues = request.args.get('predictionType')

            p = predictor.Predictor().loadModel(predictionType)

            return p.Predict(dates,logs=logs)
        @self.app.route('/api/login', methods=['POST'])

        def login():
            """Logic for login endpoint"""

        @self.app.route('/api/upload', methods=['POST'])
        def uploadFiles():
            fileType: fileUpload.FileTypes = request.args.get('fileType')
            file = request.files['file']
            if file is None:
                return "400"
            
            """Logic for file upload"""
            
            return "200"
        

    def run(self):
        port = int(os.getenv('PORT', 8080))
        self.app.run(port=port)

