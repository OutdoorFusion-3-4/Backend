from flask import request
from pkg import server

from pkg.ml.predictor import Predictor, PredictableValues


@server.route('/predictions', methods=['GET'])
def predict():
    dates = request.args.get('dates')
    logs = request.args.get('logs')
    predictionType: PredictableValues = request.args.get(
        'predictionType')

    p = Predictor().loadModel(predictionType)

    return p.Predict(dates, logs=logs)

