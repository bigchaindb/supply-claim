# -*- coding: utf-8 -*
from __future__ import print_function, absolute_import, unicode_literals

import time
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

import conf
from epcis_api.xtech_utils import add_wallet, transfer, get_wallet

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
    txid = create_st_asset(asset=asset, meta={})

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
    scan_asset = find_scan_asset(uuid)

    if scan_asset:
        return dict(
            txid=scan_asset['id'],
            code_asset_id=scan_asset['data']['fk_code']
        )

    code_id = find_code_asset_id(message)

    asset = {
        "data": {
            "name": "scan",
            "fk_code": code_id,
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
        code_asset_id=code_id
    )


def get_or_create_wallet(pub_key):
    wallet = find_wallet(pub_key)
    if wallet:
        wallet_id = wallet.get('data', {}).get('wallet_id', 'Not found')
        txid = wallet['id']
    else:
        wallet_id = add_wallet(pub_key)
        asset = {
            "data": {
                "name": "wallet",
                "pub_key": pub_key,
                "wallet_id": wallet_id,
            }
        }
        meta = {}
        txid = create_st_asset(asset, meta)

    return dict(
        txid=txid,
        wallet_id=wallet_id
    )


def get_wallet_balance(pub_key, wallet_id):
    """
    Checks the balance of a wallet. Validates if the public key matches with this specific wallet.
    """
    wallet = find_wallet(pub_key)

    if not wallet or wallet.get('data', {}).get('wallet_id', '') != wallet_id:
        return dict(error="Wallet for this user is incorrect")

    balance = get_wallet(wallet_id).get('balance', 'Error')

    return dict(
        wallet_id=wallet_id,
        balance=balance
    )


def buy_code_action(post_data):
    wallet_id = post_data['wallet_id']
    pub_key = post_data['pub_key']
    code_id = post_data['code_id']
    code_transaction = get_transaction(code_id)
    price = code_transaction.get('metadata', {}).get('scm_data', {}).get('price', None)
    if not price:
        raise Exception('Price was not set for this code.')

    transer_money_res = transfer(wallet_id, price, 'Product purchased (%s)' % int(time.time()))

    if transer_money_res.get('uuid', None) and transer_money_res.get('success', False):
        # Transfer the code ownership
        transfer_st_asset(code_id, pub_key, {})

    return transer_money_res


def create_st_asset(asset, meta=None):
    if not meta:
        meta = {}
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


def find_code_asset_id(message):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search="\"" + message + "\"")
    if result:
        for r in result:
            data = r.get('data', {})
            if data.get('message', '') == message and data.get('name', '') == 'code':
                return r['id']

    return None


def find_asset_id(message):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search="\"" + message + "\"")
    if result:
        return result[0]['id']


def find_asset(string):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search="\"" + string + "\"")
    if result:
        return result[0]
    return {}


def find_scan_asset(string):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search="\"" + string + "\"")
    if result:
        for r in result:
            if r.get('data', {}).get('name', '') == 'scan':
                return r
    return {}



def get_transaction(asset_id):
    bdb = get_bigchain_db()
    result = bdb.transactions.retrieve(asset_id)
    return result


def find_wallet(pub_key):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search="\"" + pub_key + "\"")
    for r in result:
        if r.get('data', {}).get('name', '') == 'wallet':
            return r
    return None

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
