from epcis_api import xtech_utils
import uuid


#Create a wallet and top up. Unique id generated
wallet_id = xtech_utils.add_wallet(uuid.uuid4())

amount = 800 #any number to test the transfer

if(wallet_id != 0):
    print('----Transfer----')
    xtech_utils.transfer(wallet_id, amount,'Transfer test' )    
    