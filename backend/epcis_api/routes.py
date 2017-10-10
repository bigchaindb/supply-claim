# -*- coding: utf-8 -*

from epcis_api import api
from epcis_api.api import EPCISEventAPI

api.add_resource(EPCISEventAPI, '/epcis/', endpoint='epcis')
api.add_resource(EPCISEventAPI, '/epcis/<string:id>', endpoint='epcisId')