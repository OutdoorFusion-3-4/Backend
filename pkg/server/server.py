import datetime
import dbm
import json
import operator
import os
from pkg.mapping.mappingStart import Mapping
from pkg.queries import DataQueries
from pkg.queries.types import GraphQueryParameters
import jwt
from pkg.auth import authentication
from pkg.storage.database import Database
from flask import Blueprint, Flask, Response, make_response, request,jsonify
from pkg.ml.predictor import Predictor, PredictableValues
db = Database()
port = int(os.getenv('PORT', 8080))

app = Flask(__name__)
api = Blueprint('api_routes', __name__)

app.config['SECRET_KEY'] = str(os.getenv("JWT_TOKEN","123"))

@api.before_request
def validateToken():
    if request.path == '/api/login' or request.path == '/api/register' or request.path == '/api/logout':
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
    username = request.form.get('email')
    password = request.form.get('password')
    print(username, password)
    resp = make_response()

    if authentication.Login(username, password):
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

def getFileExtension(filename):
    if '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()

ALLOWED_EXTENSIONS = {'csv', '.accdb'}

@api.route('/upload', methods=['POST'])
def uploadFiles():
    mappings = request.form.get('mapping')
    if mappings is None:
        return "400"
    mappings:dict = json.loads(mappings)
    
    for file in request.files.getlist('file'):
        if file is None:
            return "400"
        
        if getFileExtension(file.filename) not in ALLOWED_EXTENSIONS:
            return "400"
        
       

        mapping = mappings[file.filename]
        filePath = os.path.join(os.getcwd(), 'core', 'storage', 'uploads', file.filename)
        file.save(filePath)

        m = Mapping(dbm)
        try:
            m.ProcessCsv(filePath,mapping)
        except Exception as e:
            return str(e)
        finally:
            os.remove(filePath)

    return "200"



def getGraphQueryParameters() -> GraphQueryParameters:
    params = GraphQueryParameters()
    params.dateStart = request.args.get('dateStart')
    params.dateEnd = request.args.get('dateEnd')
    params.companies = request.args.get('companies')
    return params


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




@api.route('/predictions', methods=['GET'])
def predict():
    dates = request.args.get('dates')
    logs = request.args.get('logs')
    predictionType: PredictableValues = request.args.get(
        'predictionType')

    p = Predictor().loadModel(predictionType)

    return p.Predict(dates, logs=logs)

def routes():
    'Display registered routes'
    rules = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append((rule.endpoint, methods, str(rule)))

    sort_by_rule = operator.itemgetter(2)
    for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
        route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
        print(route)
app.register_blueprint(api, url_prefix='/api')
def run():
    routes()
    app.run(port=port, debug=True)

if __name__ == '__main__':
    run()
