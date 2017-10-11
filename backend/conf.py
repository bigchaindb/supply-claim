# -*- coding: utf-8 -*
from __future__ import print_function, absolute_import, unicode_literals

import os, sys
try:
    import configparser as confparser
except:
    import ConfigParser as confparser
# load the configuration

config = confparser.SafeConfigParser()
config.read("./conf/conf.cfg")

PATH = os.path.abspath(".")

MONGO_DB_NAME = config.get('database', 'name')
MONGO_PORT = int(config.get('database', 'port'))
MONGO_HOST = config.get('database', 'address')
#DATABASE_USERNAME = config.get('database', 'username')
#DATABASE_PASSWORD = config.get('database', 'password')

BIGCHAIN_DB = config.get('bigchain', 'root_url')
BIGCHAIN_PUB = config.get('bigchain', 'public_key')
BIGCHAIN_PRIV = config.get('bigchain', 'private_key')

WEBSERVER_DEBUG = int(config.get('webserver', 'debug')) == 1
WEBSERVER_HOST = config.get('webserver', 'host')
WEBSERVER_PORT = int(config.get('webserver', 'port'))