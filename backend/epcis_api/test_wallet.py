from xtech_utils import add_wallet, transfer, top_up



wallet_id = add_wallet('6sassdfc9591')

amount = 800 #any number to test

print('----Top up----')
top_up(wallet_id, 2200)
print('----Transfer----')
transfer(wallet_id, amount,'Transfer test' )





try:
    wallet_id = add_wallet('6sassdfc9591')
except IndexError:
    print('Wallet could not be created. Possible wallet id duplicated')



