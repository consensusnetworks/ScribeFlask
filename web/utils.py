from factom import Factomd, FactomWalletd
from factom.exceptions import FactomAPIError 
import json
import time 

from credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET


def createChain(twitterid, factomd, walletd):
    tweet_id = twitterid
    # factomd = factomd
    # walletd = walletd
    # factomd = Factomd(
    # host='http://18.222.184.135:8088',
    # fct_address=FCT_ADDRESS,
    # ec_address=EC_ADDRESS,
    # username='rpc_username',
    # password='rpc_password'
    # )

    # walletd = FactomWalletd(
    # host='http://18.222.184.135:8089',
    # fct_address=FCT_ADDRESS,
    # ec_address=EC_ADDRESS,
    # username='rpc_username',
    # password='rpc_password'
    # )

    try:
        resp = walletd.new_chain(factomd,
                            [ 'TwitterBank Record',str(tweet_id), 'refactor378'],
                            'This is the start of this users TwitterBank Records', 
                            ec_address=EC_ADDRESS) 
        print(resp)             
        chain_ID = resp['chainid']
        print(chain_ID)
        time.sleep(1)
        

    except FactomAPIError as e:
        print(e.data)
        print('ERROR')
        return e.data

    return chain_ID