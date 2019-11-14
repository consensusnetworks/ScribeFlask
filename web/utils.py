from factom import Factomd, FactomWalletd, exceptions #python Factom API
import json

from credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
# print(FCT_ADDRESS,EC_ADDRESS)

def createChain(twitterid):
    tweet_id = str(twitterid)
    print(tweet_id)
    fct_address = FCT_ADDRESS
    ec_address = EC_ADDRESS
    print(ec_address)

    factomd = Factomd(
    host='http://18.222.184.135:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
    )

    walletd = FactomWalletd(
    host='http://18.222.184.135:8089',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
    )

    try:
        walletd.new_chain(factomd, 
                                [ "random",'chain', "idqqqqq"],
                                "This is a test", ec_address=ec_address) 
                        
        # chain_ID = resp['chainid']
        # print(chain_ID)
        # time.sleep(1)
        # print(factomd.entry_credit_balance(ec_address))

    except exceptions.FactomAPIError as e:
        data = e.data
        print(data )
        print('ERROR')
        return True

    # return chain_ID