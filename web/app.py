import bcrypt
import json
import os
from pymongo import MongoClient
import time

from factom import Factomd, FactomWalletd
from factom.exceptions import FactomAPIError 
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from kafka import SimpleProducer, KafkaClient, KafkaConsumer

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

client = MongoClient("mongodb://db:27017")
db = client.ScribeDatabase
users = db["Users"]

class UserRegistration(Resource):
    def post(self):
        #step 1 get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"]

        correct_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and password in database
        users.insert({
            "Username": username,
            "Password": correct_pw,
            "Accounts":[]
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API",
        }

        return jsonify(retJson)
        
def verifyPw(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else: 
        return False

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

api.add_resource(UserRegistration, '/register')
api.add_resource(TwitterAccount, '/twitteraccounts')
@app.route('/')
def hello_world():
    return "Hello World!"
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
