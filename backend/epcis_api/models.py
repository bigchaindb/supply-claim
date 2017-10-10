# -*- coding: utf-8 -*-

from flask_mongoengine import Document
from datetime import datetime
import bson.objectid
from mongoengine import ObjectIdField, DictField, DateTimeField, IntField, StringField


class EPCISEvent(Document):
    """
    Defines the model for an EPCIS event.
    """
    oid = ObjectIdField(default=bson.objectid.ObjectId, primary_key=True)
    data = DictField()
    insertion_date = DateTimeField(required=True, default=datetime.now)

    def __str__(self):
        return 'ECISEvent: %s' % self.data


class Company(Document):
    oid = ObjectIdField(default=bson.objectid.ObjectId, primary_key=True)
    company_id = IntField(required=True, min_value=0, unique=True)
    slug = StringField(required=True)
    bigchain_public_key = StringField(required=False, default='')
    bigchain_private_key = StringField(required=False, default='')

    creation_date = DateTimeField(required=True, default=datetime.now)

    def __str__(self):
        return 'Company: %s' % self.id