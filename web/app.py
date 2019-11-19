from factom import Factomd, FactomWalletd
from factom.exceptions import FactomAPIError 
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json
from kafka import SimpleProducer, KafkaClient, KafkaConsumer

from credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from utils import createChain
app = Flask(__name__)
api = Api(app)

class TwitterAccount(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()
        print(postedData)
        #Step 2 is to read the data
        handle = postedData["handle"]
        twitterid = str(postedData["twitter_id"])
        print(handle, twitterid)

        retJSON = {
            'Message': twitterid + " successfully added!",
            'Status Code': 200
        }

        chain_id = createChain(twitterid=str(twitterid))
        print(chain_id)

        return jsonify(retJSON)


api.add_resource(TwitterAccount, '/twitteraccounts')
@app.route('/')
def hello_world():
    return "Hello World!"
if __name__=="__main__":
    app.run(host='localhost')