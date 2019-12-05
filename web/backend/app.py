import bcrypt
import json
import logging
from datetime import datetime
import os
from pymongo import MongoClient
import time

from factom import Factomd, FactomWalletd
from factom.exceptions import FactomAPIError 
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from kafka import SimpleProducer, KafkaClient, KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

from config import config
from utils import createChain

conf = config[os.environ.get('SCRIBE_CONFIG', 'development')]
factom_url = conf.FACTOM_BASE_URL
wallet_url = conf.WALLET_BASE_URL
ec_address = conf.EC_ADDR
fct_address = conf.FC_ADDR
kafka_url = conf.KAFKA_URL

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'

api = Api(app)
jwt = JWTManager(app)
# client = MongoClient("mongodb://db:27017")
client = MongoClient("mongodb://db:27017")

db = client.ScribeDatabase
users = db["Users"]

CORS(app)

class UserRegistration(Resource):
    def post(self):
        #step 1 get posted data by the user
        postedData = request.get_json()
        print(postedData)
        #Get the data
        username = postedData["Username"]
        password = postedData["Password"]
        correct_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        email = postedData["email"]
        created = datetime.utcnow()
        # Store username and password in database
        user_id = users.insert({
            "Username": username,
            "Password": correct_pw,
            "email": email,
            "created": created,
            "Accounts":[]
        })

        new_user = users.find_one({'_id': user_id})
        retJson = {
            "status": 200,
            "msg": new_user["email"] + ' registered',
        }

        return jsonify(retJson)
class UserLogin(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["Username"]
        password = postedData["Password"]
        result = ""

        response = users.find_one({"Username": username})

        if response:
            if bcrypt.checkpw( password.encode('utf8'), response["Password"]):
                access_token = create_access_token(identity = {
                    "username": response["Username"],
                    "email": response["email"]
                })
                result = jsonify({"token": access_token})
            else: 
                result = jsonify({"error": "Invalid username and password"})
        else:
            result = jsonify({"result": "No results found"})

        return result
class TwitterAccount(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()

        print(postedData)
        #Step 2 is to read the data
        username = users.find_one("Username")
        # password = postedData["password"]
        handle = postedData["handle"]
        twitterid = str(postedData["twitterid"])

        # Step3 Generate Chain for Twitter Account
        factomd = Factomd(host=factom_url, ec_address=ec_address, fct_address=fct_address, username='rpc_username',password='rpc_password')
        walletd = FactomWalletd(host=wallet_url, ec_address=ec_address, fct_address=fct_address, username='rpc_username',password='rpc_password')
        print(factomd, walletd)
        try:
            resp = walletd.new_chain(factomd,[ 'TwitterBank Record',str(twitterid), 'fulltest7'],
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

        # Step 4 Store the Account in the database for a user
        users.update({
            "Username":username,
        }, {
            "$set": {
                    "Accounts":[
                        {
                            "handle": handle,
                            "twitterid": twitterid,
                            "chainid": chainid,
                            "tracking": ""
                        }
                    ]
                }
        })
        retJSON = {
            'handle': handle,
            'twitterid': twitterid,
            'chainid': str(chainid),
        }

        return jsonify(retJSON)

class Track(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()

        #Step 2 is to read the data
        # username = postedData["username"]
        # password = postedData["password"]
        handle = postedData["handle"]
        twitterid = str(postedData["twitter_id"])
        chainid = postedData["chainid"]

        #Step 3 verify the username pw match
        
        # Step 4 get the twitterid for the account you want to track
        twitteraccount = users.find_one({"Accounts.twitterid": twitterid})
        account = twitteraccount['Accounts']
        taccount = account[0]

        #Step 4 Send Account object to Kafka
        kafka = KafkaClient("kafka:9093")
        # client=KafkaClient('localhost:9092')
        producer = SimpleProducer(kafka, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        try:
            logging.info('sending message %s to kafka', chainid)
            producer.send_messages('Scribe', json.dumps(taccount).encode('utf-8'))
            # producer.send('Scribe', taccount)
            logging.info('%s sent!', taccount)
        except KafkaError as error:
            logging.warning('The message was not sent to the mempool, caused by %s', error)

        print('Sending Condition to Mempool!')

        #Step 4 Store the Account in the database for a user
        users.update({
            "Username":username,
        }, {
            "$set": {
                    "Accounts":[
                        {
                            "handle": handle,
                            "twitterid": twitterid,
                            "chainid": chainid,
                            "tracking": "yes"
                        }
                    ]
                }
        })
        retJSON = {
            'Message': str(taccount) + " successfully tracked!",
            'Status Code': 200
        }

        return jsonify(retJSON)

api.add_resource(UserLogin, '/users/login')
api.add_resource(UserRegistration, '/users/register')
api.add_resource(TwitterAccount, '/users/twitteraccounts')
api.add_resource(Track, '/users/twitteraccounts/track')
@app.route('/')
def hello_world():
    return "Hello World!"
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
