from factom import Factomd, FactomWalletd
from factom.exceptions import FactomAPIError 
import json
import time 

def createChain(twitterid, factomd, walletd):
    tweet_id = twitterid

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