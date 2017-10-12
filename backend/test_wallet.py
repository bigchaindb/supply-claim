from epcis_api import xtech_utils
import uuid


#Create a wallet and top up. Unique id generated
wallet_uuid = xtech_utils.add_wallet(uuid.uuid4())

print('----GET_WALLET----')
xtech_utils.get_wallet(wallet_uuid)

amount = 800 #any number to test the transfer
if(wallet_uuid != 0):
    print('----Transfer----')
    xtech_utils.transfer(wallet_uuid, amount,'Transfer test' )    
    