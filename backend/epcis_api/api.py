# -*- coding: utf-8 -*-
from datetime import datetime

from mongoengine import DoesNotExist
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort

from epcis_api import models, validators, bigchain_utils
from epcis_api.models import Company


class EPCISEventAPI(Resource):
    def __init__(self):
        super(EPCISEventAPI, self).__init__()

    def get(self, id=None):
        """
        Return one or list EPCIS events
        """
        if id:
            result = models.EPCISEvent.objects.get_or_404(oid=id)
            return jsonify(result)
        else:
            try:
                page = int(request.args['page'])
            except:
                page = 1
            total = models.EPCISEvent.objects.count()
            result = models.EPCISEvent.objects.paginate(page=page, per_page=100)

            if len(result.items) == 0:
                return jsonify(result="no epcis event")

        return jsonify(count=total, epcis_events=result.items)

    # def put(self):
    #     """
    #     Accept a XML file... no validations
    #     """
    #     xml_epcis_event = request.data
    #     json_epcis_event = parse(xml_epcis_event)
    #     models.EPCISEvent(data=json_epcis_event).save()
    #     return json_epcis_event

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, required=True)
        parser.add_argument('bizLocation', type=validators.location_validator, required=False)
        parser.add_argument('bizStep', type=str, required=True)
        parser.add_argument('disposition', type=str, required=True)
        parser.add_argument('epcList', type=validators.epc_validator, required=True)
        parser.add_argument('eventTime', type=str, required=True)
        parser.add_argument('readPoint', type=validators.readpoint_validator, required=False)
        parser.add_argument('company_id', type=int, required=True)
        # parser.add_argument('recordTime', type=str, required=True)
        result = parser.parse_args()

        company = None
        try:
            company = Company.objects.get(company_id=result['company_id'])
        except DoesNotExist:
            abort(404, error="Company not registered")

        result['recordTime'] = str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        e = models.EPCISEvent(data=result).save()

        bigchain_utils.insert_event(e.oid, company)

        response = {
            'result': result,
            'oid': str(e.oid)
        }
        return response
