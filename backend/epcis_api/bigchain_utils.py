# -*- coding: utf-8 -*
from __future__ import print_function, absolute_import, unicode_literals

from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

import conf

PUB_KEY = conf.BIGCHAIN_PUB
PRIV_KEY = conf.BIGCHAIN_PRIV

def get_bigchain_db():
    bdb_root_url = conf.BIGCHAIN_DB
    return BigchainDB(bdb_root_url)


def get_keypair():
    key = generate_keypair()
    return key.public_key, key.private_key


def onboard_user(pub_key, install_id):
    asset = {
        "data": {
            "name": "user_onboarding",
            "pub_key": pub_key,
            "install_id": install_id
        }
    }
    txid = create_st_asset(asset=asset)

    return dict(
        name="user_onboarding",
        pub_key=pub_key,
        install_id=install_id,
        txid=txid
    )


def insert_code(code):
    asset = {
        "data": code
    }
    txid = create_st_asset(asset=asset)

    return dict(
        txid=txid
    )


def create_st_asset(asset):
    bdb = get_bigchain_db()

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=PUB_KEY,
        asset=asset
    )
    fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=PRIV_KEY)
    bdb.transactions.send(fulfilled_creation_tx)

    return fulfilled_creation_tx['id']

# def insert_event(event_id, company):
#     bdb = get_bigchain_db()
#     asset = {
#         "data": {
#             "event_id": str(event_id)
#         }
#     }
#     prepared_creation_tx = bdb.transactions.prepare(
#         operation='CREATE',
#         signers=company.bigchain_public_key,
#         asset=asset
#     )
#     fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=company.bigchain_private_key)
#     sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)
#     txid = fulfilled_creation_tx['id']
#     print(txid)
#
#     bdb.transactions.status(txid)
