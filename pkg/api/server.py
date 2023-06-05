
import datetime
import os
from ..storage.database import Database
import os
import jwt
from flask import Flask, request, make_response, Response, Blueprint, jsonify
from ..fileUpload import fileUpload
from core.ml import predictor
from pkg.api import authentication
from pkg.queries.DataQueries import DataQueries
from pkg.queries.types import GraphQueryParameters
from core.mapping.mappingStart import Mapping

db = Database()
port = int(os.getenv('PORT', 8080))

ALLOWED_EXTENSIONS = {'csv', '.accdb'}
api = Blueprint('api_routes', __name__,
                template_folder='api')
def getFileExtension(filename):
    if '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()

def getGraphQueryParameters() -> GraphQueryParameters:
    params = GraphQueryParameters()
    params.dateStart = request.args.get('dateStart')
    params.dateEnd = request.args.get('dateEnd')
    params.companies = request.args.get('companies')
    return params


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


@api.route('/upload', methods=['POST'])
def uploadFiles():
    file = request.files['file']
    if file is None:
        return "400"
    
    if getFileExtension(file.filename) not in ALLOWED_EXTENSIONS:
        return "400"
    
    mapping = request.form.get('mapping')
    if mapping is None:
        return "400"

    filePath = os.path.join(os.getcwd(), 'core', 'storage', 'uploads', file.filename)
    file.save(filePath)

    m = Mapping(db)
    try:
        m.ProcessCsv(filePath,mapping)
    except Exception as e:
        return str(e)
    finally:
        os.remove(filePath)

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
