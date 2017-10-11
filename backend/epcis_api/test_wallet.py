from xtech_utils import add_wallet, transfer, top_up
import uuid


#Create a wallet and top up. Unique id generated
wallet_id = add_wallet(uuid.uuid4())

amount = 800 #any number to test the transfer

if(wallet_id != 0):
    print('----Transfer----')
    transfer(wallet_id, amount,'Transfer test' )









