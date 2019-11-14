from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json
from kafka import SimpleProducer, KafkaClient, KafkaConsumer

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
        twitterid = postedData["twitter_id"]
        print(handle, twitterid)

        retJSON = {
            'Message': twitterid + " successfully added!",
            'Status Code': 200
        }

        chain_id = createChain(twitterid=twitterid)
        print(chain_id)

        return jsonify(retJSON)


api.add_resource(TwitterAccount, '/twitteraccounts')
@app.route('/')
def hello_world():
    return "Hello World!"
if __name__=="__main__":
    app.run(host='localhost')