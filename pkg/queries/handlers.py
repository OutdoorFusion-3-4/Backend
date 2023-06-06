from flask import request
from pkg.queries import DataQueries
from pkg.queries.types import GraphQueryParameters
from pkg.server.server import db, api
from flask import request, jsonify

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

