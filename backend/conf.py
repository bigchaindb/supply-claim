# -*- coding: utf-8 -*
from __future__ import print_function, absolute_import, unicode_literals

import os, sys
try:
    import configparser as confparser
except:
    import ConfigParser as confparser
# load the configuration

config = confparser.SafeConfigParser()
config.read("app.cfg")

PATH = os.path.abspath(".")

MONGO_DB_NAME = config.get('mongo', 'db_name')
MONGO_PORT = int(config.get('mongo', 'port'))
MONGO_HOST = config.get('mongo', 'host')
#DATABASE_USERNAME = config.get('database', 'username')
#DATABASE_PASSWORD = config.get('database', 'password')

BIGCHAIN_DB = config.get('bigchain', 'root_url')
BIGCHAIN_PUB = config.get('bigchain', 'public_key')
BIGCHAIN_PRIV = config.get('bigchain', 'private_key')

WEBSERVER_DEBUG = int(config.get('webserver', 'debug')) == 1
WEBSERVER_HOST = config.get('webserver', 'host')
WEBSERVER_PORT = int(config.get('webserver', 'port'))

XTECH_END = config.get('xtech', 'base_endpoint')
XTECH_GETW = config.get('xtech', 'get_wallet_key')
XTECH_TRANS = config.get('xtech', 'transfer_key')
XTECH_DEFW = config.get('xtech', 'default_wallet')