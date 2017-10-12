import requests
import json
import uuid
import conf

ENDPOINT = conf.XTECH_END
GET_WALLET = conf.XTECH_END + conf.XTECH_GETW
TRANS = conf.XTECH_END + conf.XTECH_TRANS
DEF_WALLET = conf.XTECH_DEFW


def add_wallet(public_key):
    add_wallet_url = ENDPOINT + 'addwallet'
    payload = {'user_id': public_key}
    r = requests.post(add_wallet_url, payload)
    response = r.json()
    resp_data = ''
    try:
        resp_data = response['data'][0]
    except IndexError:
        print('Error: Wallet not created. Possible wallet id duplicated.')
        return 0
    
    print('----Top up----')
    top_up(resp_data['uuid'], 25)
    print('Wallet UUID: ' + resp_data['uuid'])
    return resp_data['uuid']


def get_wallet(wallet_uuid):
    payload = {'uuid': wallet_uuid}
    r = requests.post(GET_WALLET, payload)
    response = r.json()
    resp_data = ''
    try:
        resp_data = response['data'][0]
    except IndexError:
        print('Error: Could not get wallet.')
        return 0
    print('Wallet UUIID '+resp_data['uuid']+ ', Balance: ' + str(resp_data['total_balance']))
    return {
        'wallet_uuid':resp_data['uuid'],
        'balance':resp_data['total_balance'],
        'user_id':resp_data['user_id']
    }


def transfer(wallet_uuid, amount, reference):
    return call_transfer(wallet_uuid, DEF_WALLET, amount, reference)


def top_up(wallet_uuid, amount):
    return call_transfer(DEF_WALLET, wallet_uuid, amount, 'top-up wallet')


def call_transfer(wallet_uuid_from, wallet_uuid_to, amount, reference):
    payload = {'order_id': uuid.uuid4(), 
               'from_wallet': wallet_uuid_from, 
	       'to_wallet': wallet_uuid_to,
	       'amount': amount,
	       'reference': reference}
    r = requests.post(TRANS, payload)
    response = r.json()
    #in case there is an error
    print('Error transfering: ' + str(response['error']))
    print('TRX UUID: ' + str(response))
    resp_data = response['data']
    
    
    
    txid = None
    new_balance = None
    insufficient_funds = False
    if not(response['error']):
        print('TRX UUID: ' + resp_data['uuid'])
        txid = resp_data['uuid']
        new_balance = get_wallet(wallet_uuid_from)['balance']
    else:
        insufficient_funds = response['msg_trans'] == 'negative_source_wallet'
        if insufficient_funds:
            new_balance = get_wallet(wallet_uuid_from)['balance']
    
    resp = {
        'success': not response['error'],
        'insufficient_funds': insufficient_funds,
        'txid': txid,
        'new_balance': new_balance
    }
    return resp
