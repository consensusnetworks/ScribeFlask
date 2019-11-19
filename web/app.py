from factom import Factomd, FactomWalletd
from factom.exceptions import FactomAPIError 
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json
import os
import time

from kafka import SimpleProducer, KafkaClient, KafkaConsumer

from credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from config import config
from utils import createChain

conf = config[os.environ.get('SCRIBE_CONFIG', 'development')]
factom_url = conf.FACTOM_BASE_URL
wallet_url = conf.WALLET_BASE_URL
ec_address = conf.EC_ADDR
fct_address = conf.FC_ADDR
print(factom_url, wallet_url, ec_address, fct_address)

app = Flask(__name__)
api = Api(app)

# factomd = Factomd(
#     host='http://18.222.184.135:8088',
#     fct_address=FCT_ADDRESS,
#     ec_address=EC_ADDRESS,
#     username='rpc_username',
#     password='rpc_password'
#     )

# walletd = FactomWalletd(
#     host='http://18.222.184.135:8089',
#     fct_address=FCT_ADDRESS,
#     ec_address=EC_ADDRESS,
#     username='rpc_username',
#     password='rpc_password'
#     )

class TwitterAccount(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()

        print(postedData)
        #Step 2 is to read the data
        handle = postedData["handle"]
        twitterid = str(postedData["twitter_id"])
        print(handle, twitterid)

        #Step3 Generate Chain for Twitter Account
        factomd = Factomd(host=factom_url, ec_address=ec_address, fct_address=fct_address, username='rpc_username',password='rpc_password')
        walletd = FactomWalletd(host=wallet_url, ec_address=ec_address, fct_address=fct_address, username='rpc_username',password='rpc_password')
        print(factomd, walletd)
        try:
            resp = walletd.new_chain(factomd,[ 'TwitterBank Record',str(twitterid), 'refactor8'],
                                    'This is the start of this users TwitterBank Records', 
                                    ec_address=ec_address) 
            print(resp)             
            chain_ID = resp['chainid']
            print(chain_ID)
            chainid = chain_ID

        except FactomAPIError as e:
            print(e.data)
            print('ERROR')
            chainid = str(e.data)


        retJSON = {
            'Message': chainid + " successfully created!",
            'Status Code': 200
        }

        return jsonify(retJSON)


api.add_resource(TwitterAccount, '/twitteraccounts')
@app.route('/')
def hello_world():
    return "Hello World!"
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
