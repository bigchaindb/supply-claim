#! /usr/bin/env python
# -*- coding: utf-8 -*
from cerberus import Validator
from flask import json


def location_validator(value):
    LOCATION_SCHEMA = {
        'id': {'required': True, 'type': 'string'}
    }
    v = Validator(LOCATION_SCHEMA)
    if v.validate(value):
        return value
    else:
        raise ValueError(json.dumps(v.errors))


def epc_validator(value):
    EPC_SCHEMA = {
        'epc': {'required': True, 'type': 'string'}
    }
    v = Validator(EPC_SCHEMA)
    if v.validate(value):
        return value
    else:
        raise ValueError(json.dumps(v.errors))


def readpoint_validator(value):
    READPOINT_SCHEMA = {
        'id': {'required': True, 'type': 'string'}
    }
    v = Validator(READPOINT_SCHEMA)
    if v.validate(value):
        return value
    else:
        raise ValueError(json.dumps(v.errors))