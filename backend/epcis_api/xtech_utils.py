import requests
import json
import uuid
import conf

ENDPOINT = conf.XTECH_END
TRANS = conf.XTECH_END + conf.XTECH_TRANS
DEF_WALLET = conf.XTECH_DEFW


def add_wallet(public_key):
    add_wallet_url = ENDPOINT + 'addwallet'
    payload = {'user_id': public_key}
    r = requests.post(add_wallet_url, payload)
    response = r.json()
    #in case there is an error
    print('Error adding wallet: ' + str(response['error']))
    resp_data = ''
    try:
        resp_data = response['data'][0]
    except IndexError:
        print('Error: Wallet not created. Possible wallet id duplicated.')
        return 0
    
    
    print('----Top up----')
    top_up(resp_data['uuid'], 2200)
    print('Wallet UUID: ' + resp_data['uuid'])
    return resp_data['uuid']


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
    resp_data = response['data']
    
    resp_data = ''
    try:
        resp_data = response['data']
    except IndexError:
        print('Error: Transfer not done. Possible wallet id or transfer id duplicated.')
        return 0
    
    
    print('TRX UUID: ' + resp_data['uuid'])
    return resp_data['uuid']
