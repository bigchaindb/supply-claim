# ScanTrust EPCIS API

ScanTrust EPCIS API is an API that enables EPCIS events to be stored and transactions to be managed by __BigchainDB__.

  - Flask API app
  - MongoDB centralized database
  - Partly decentralized BigchaibDB

### More Information
---
  - [Trello](https://trello.com/b/II8PmbsM/blockchain) - Blockchain Trello board
  - [Flask](http://flask.pocoo.org/) - Flask (A Python micro framework)
  - [BigchainDB](https://www.bigchaindb.com/) - BigchainDB partly decentralized database

### Installation
---
__Requirements:__
  - Python 3.5+
  - MongoDB
  - BigchainDB

```sh
(virtualenv)$ cd epcis-api
(virtualenv)$ pip install -r requirements.txt
```
Edit *epcis/conf/sample_conf.cfg* and copy to *epcis/conf/__conf.cfg__*

### Usage
---
Run a local test server:
```sh
(virtualenv)$ ./runserver.py
```