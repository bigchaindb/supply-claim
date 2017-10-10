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

DATABASE_NAME = config.get('database', 'name')
DATABASE_PORT = int(config.get('database', 'port'))
DATABASE_ADDRESS = config.get('database', 'address')
#DATABASE_USERNAME = config.get('database', 'username')
#DATABASE_PASSWORD = config.get('database', 'password')

BIGCHAIN_DB = config.get('bigchain', 'root_url')

WEBSERVER_DEBUG = int(config.get('webserver', 'debug')) == 1
WEBSERVER_HOST = config.get('webserver', 'host')
WEBSERVER_PORT = int(config.get('webserver', 'port'))