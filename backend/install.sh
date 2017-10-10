#!/bin/bash

# Installation of MongoDB
sudo apt-get install -y mongodb-server
sudo service mongodb start

# Python dependencies
sudo apt-get install -y python-pip
pip install --user virtualenv
virtualenv --no-site-packages ./env_EPC_Information_Service
source ./env_EPC_Information_Service/bin/activate
pip install --upgrade -r requirements.txt

# Configuration
cp conf/conf.cfg-sample conf/conf.cfg

# Launch the server
python runserver.py

deactivate
