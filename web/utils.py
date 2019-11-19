from factom import Factomd, FactomWalletd
from factom.exceptions import FactomAPIError 
import json

from credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET

def createChain(twitterid):
    tweet_id = twitterid
    factomd = Factomd(
    host='http://18.222.184.135:8088',
    fct_address=FCT_ADDRESS,
    ec_address=EC_ADDRESS,
    username='rpc_username',
    password='rpc_password'
    )

    walletd = FactomWalletd(
    host='http://18.222.184.135:8089',
    fct_address=FCT_ADDRESS,
    ec_address=EC_ADDRESS,
    username='rpc_username',
    password='rpc_password'
    )

    try:
        resp = walletd.new_chain(factomd,
                            [ 'TwitterBank Record',str(tweet_id), 'refactor378'],
                            'This is the start of this users TwitterBank Records', 
                            ec_address=EC_ADDRESS) 
        print(resp)             
        chain_ID = resp['chainid']
        print(chain_ID)
        time.sleep(1)
        # print(factomd.entry_credit_balance(ec_address))

    except FactomAPIError as e:
        print(e.data)
        print('ERROR')
        return True

    # return chain_ID