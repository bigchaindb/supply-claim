# -*- coding: utf-8 -*
from __future__ import print_function, absolute_import, unicode_literals

import time
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
        "data": {
            "name": "code",
            "message": code.pop('message'),
            "workorder": code.pop('workorder', ''),
            "product": code.pop('product', ''),
            "serial_number": code.pop('serial_number', ''),
            "sequence": code.pop('sequence', '')
        }
    }

    metadata = code

    txid = create_st_asset(asset=asset, meta=metadata)

    return dict(
        txid=txid
    )


def insert_scan(scan):
    message = scan.pop('message')
    uuid = scan.get('uuid')
    scan_asset = find_asset(uuid)

    if scan_asset:
        return dict(
            txid=scan_asset['id'],
            code_asset_id=scan_asset['data']['fk_code']
        )

    id = find_asset_id(message)

    asset = {
        "data": {
            "name": "scan",
            "fk_code": id,
            "uuid": uuid,
            "lat": scan.get('lat', ''),
            "lng": scan.get('lng', ''),
            "timestamp": int(time.time())
        }
    }

    metadata = {}

    txid = create_st_asset(asset=asset, meta=metadata)

    return dict(
        txid=txid,
        code_asset_id=id
    )


def create_st_asset(asset, meta):
    bdb = get_bigchain_db()
    meta['timestamp'] = int(time.time())
    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=PUB_KEY,
        asset=asset,
        metadata=meta
    )
    fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=PRIV_KEY)
    bdb.transactions.send(fulfilled_creation_tx)

    return fulfilled_creation_tx['id']


def transfer_asset_to_self(txid, meta):
    """
    Used to edit metadata on a code
    """
    transfer_st_asset(txid, PUB_KEY, meta)


def transfer_st_asset(txid, to_pub_key, meta):
    bdb = get_bigchain_db()
    meta['timestamp'] = int(time.time())
    input_tx = bdb.transactions.retrieve(txid)

    prepared_transfer_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        inputs={
            'fulfillment': input_tx['outputs'][0]['condition']['details'],
            'owners_before': input_tx['outputs'][0]['public_keys'],
            'fulfills': {
                'txid': input_tx['id'],
                'output': 0
            }
        },
        recipients=to_pub_key,
        metadata=meta
    )
    fulfilled_tx = bdb.transactions.fulfill(
        prepared_transfer_tx,
        private_keys=PRIV_KEY
    )
    bdb.transactions.send(fulfilled_tx)

    return fulfilled_tx['id']


def find_asset_id(message):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search=message)
    if result:
        return result[0]['id']


def find_asset(string):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search=string)
    if result:
        return result[0]

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
