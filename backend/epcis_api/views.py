#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_restful import reqparse
from mongoengine import NotUniqueError
from epcis_api import app, models
from epcis_api.bigchain_utils import get_keypair, onboard_user


@app.route('/', methods=['GET'])
def index():
    """
    """
    return jsonify({})


@app.route('/api/register/company/', methods=['POST'])
def register_company():
    parser = reqparse.RequestParser()
    parser.add_argument('company_id', type=int, required=True)
    parser.add_argument('slug', type=str, required=True)
    request_params = parser.parse_args()

    result = request_params
    public_key, private_key = get_keypair()

    try:
        models.Company(company_id=result['company_id'],
                       slug=result['slug'],
                       bigchain_public_key=public_key,
                       bigchain_private_key=private_key
                       ).save()
    except NotUniqueError:
        return jsonify(error="Company already registered"), 400

    return jsonify(data="ok")


@app.route('/api/register/onboard/', methods=['POST'])
def onboard():
    """
    Save the install_id and pub_key as an asset in DBD, setting ST as the owner.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('pub_key', type=str, required=True)
    parser.add_argument('install_id', type=str, required=True)
    request_params = parser.parse_args()

    result = onboard_user(request_params['pub_key'], request_params['install_id'])

    return jsonify(result)


# @app.route('/what/<string:epc>', methods=['GET'])
# def what(epc=None):
#     """
#     Returns all EPCIS events involving the electronic product code (EPC)
#     given in parameter.
#     """
#     result = models.EPCISEvent.objects(data__ObjectEvent__epcList__epc=epc).only("data")
#     if result.count() == 0:
#         return jsonify(result="no epcis event", nb_items=result.count())
#     epcis_events = [epcis_api.data for epcis_api in result]
#     return jsonify(result="ok", nb_items=result.count(), epcis_events=epcis_events)
#
#
# @app.route('/where/<string:location>', methods=['GET'])
# def where(location=None):
#     """
#     Return all EPCIS events at 'bizLocation'.
#     """
#     result = models.EPCISEvent.objects(data__ObjectEvent__bizLocation__id=location).only("data")
#     if result.count() == 0:
#         return jsonify(result="no epcis event", nb_items=result.count())
#     epcis_events = [epcis_api.data for epcis_api in result]
#     return jsonify(result="ok", nb_items=result.count(), epcis_events=epcis_events)
#
#
# @app.route('/query/', methods=['GET'])
# def query():
#     """
#     Return all EPCIS events matching the request received in parameter.
#     """
#     query_string, value = request.args.get('query'), request.args.get('value')
#     result = models.EPCISEvent.objects(**{"data__"+query_string: value}).only("data")
#     if result.count() == 0:
#         return jsonify(result="no epcis event", nb_items=result.count())
#     epcis_events = [epcis_api.data for epcis_api in result]
#     return jsonify(result="ok", nb_items=result.count(), epcis_events=epcis_events)


@app.errorhandler(404)
def not_found(error=None):
    """
    Handles 404 errors.
    """
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
