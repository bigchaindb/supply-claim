#! /usr/bin/env python
# -*- coding: utf-8 -*
import flask_restful
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine


import conf

# Create Flask application
app = Flask(__name__)
app.debug = True

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'qsdkqlsdjfghhliqjkyezgkjl'

app.config['MONGODB_SETTINGS'] = {
    'db': conf.MONGO_DB_NAME,
    'host': conf.MONGO_HOST,
    'port': conf.MONGO_PORT
}

# Allow CORS requests
CORS(app)

# Initializes the database
db = MongoEngine()
db.init_app(app)

# REST Web service

api = flask_restful.Api(app=app)

import epcis_api.views
# import epcis_api.rest
import epcis_api.routes