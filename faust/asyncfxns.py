from factom import Factomd, FactomWalletd, exceptions #python Factom API
from kafka import SimpleProducer, KafkaClient, KafkaConsumer

import csv
from datetime import datetime
import identitykeys
import json
import os
import pandas as pd
import sys
import time
import tweepy

from config import config

conf = config[os.environ.get('SCRIBE_CONFIG', 'development')]
factom_url = conf.FACTOM_BASE_URL
wallet_url = conf.WALLET_BASE_URL
ec_address = conf.EC_ADDR
fct_address = conf.FC_ADDR
TWITTER_KEY = conf.TWITTER_KEY
TWITTER_SECRET = conf.TWITTER_SECRET
TWITTER_APP_KEY = conf.TWITTER_APP_KEY
TWITTER_APP_SECRET = conf.TWITTER_APP_SECRET

from utils import filterTweets, getAllTweets, sendTweets, filterTweets, getAllTweets, fromCreator, getKeys, getTwitterCredentials, reconstructTweet

private_key, public_key = identitykeys.generate_key_pair()
private = private_key.to_string()
public = public_key.to_string()
message = b'TwitterBank Record'
signature = private_key.sign(message)

factomd = Factomd(host=factom_url, ec_address=ec_address, fct_address=fct_address, username='rpc_username',password='rpc_password')
walletd = FactomWalletd(host=wallet_url, ec_address=ec_address, fct_address=fct_address, username='rpc_username',password='rpc_password')
#### Consolidates Tweets from an Accounts Timeline into a CSV file that can then be written to Factom
async def tweetFetcher(handle, chainid):

    handle = handle # topic == twitter handle

    auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET) #Gathers Twitter Keys
    auth.set_access_token(TWITTER_APP_KEY, TWITTER_APP_SECRET) #Gathers Twitter APP Keys
    api = tweepy.API(auth)
    print('Fetching tweets')
    getAllTweets(handle) #fetches up to 3120 most recent tweets from a users timeline & creates a csv file of them
    print('Tweets Fetched')
    cwd = os.getcwd()
    print(cwd)

    for file in os.listdir(cwd):
        print(file)
        if file.endswith('.csv'):
            new_file = filterTweets(file) #filters the csv file so that only tweets from the account being tracked are present i.e no retweets, replies to their tweets, etc.
            os.remove(file)
            print(new_file)
            data = pd.read_csv(new_file) #reads a csv file of tweets
            df = pd.DataFrame(data)

            df_ids = df['id'] #defines a data frame object of only the row in the csv with tweetids

            for tweetid in df_ids:
                status = reconstructTweet(tweetid)
                userid = status.user.id
                user_id = str(userid).replace("'", '"')
                tweet_id = str(tweetid).replace("'", '"')
                fct_entry = {'Date_Recorded': str(datetime.now()),
                            'tweet': status._json}
                try:
                    resp = walletd.new_entry(factomd, chain_id, 
                                                [ 'TwitterBank Record',user_id, tweet_id ,public, signature],
                                                str(fct_entry), ec_address=ec_address) # makes entry into the factom testnet
                    
                    print(' Tweet Successfully Entered Into the Factom Testnet!')
                    print(resp)
                except exceptions.FactomAPIError as e:
                    print(e.data)

"""
This file defines the stream listern object that is used to track a speciied twitter account and send only tweet ids from his or her
original tweets to a kafka message queue using a kafka producer that can then be consumed at a later time so that they may be used
to write tweets to the factom blockchain. This class uses several functions from the HelperFxns.py file, so if you may find further
documentation on them there.
"""
class StreamListener(tweepy.StreamListener):

    def field_load(self, handle, twitterid, chain_id):
        self.twitterid = twitterid
        self.chain_id = chain_id
        self.handle = handle
        # self.ec_address = ec_address
        # self.fct_address = fct_address

        print(self.twitterid, self.chain_id, self.handle)

    def on_status(self, status):  #Tweets will need to be filtered, twitter default pulls ALL tweets with the username you're tracking
        
        if fromCreator(status): #filters tweets related to an account so only the original tweets trigger a response
            
            print('Tweet Filtered!')
            
            try:

                userid = status.user.id
                user_id = str(userid).replace("'", '"')
                print(str(userid))

                tweetid = str(status.id)
                tweet_id = str(tweetid).replace("'", '"')
                print(tweetid)

                name = status.user.screen_name #pulls username of tweeter
                print('@',name, 'tweeted', status.text) #prints tweet to terminal
                date = datetime.now()
                
                chain_id = str(self.chain_id)
                print(chain_id)
                topic = self.handle
                
                fct_entry = {'Date_Recorded': str(datetime.now()),
                            'tweet': status._json}
                print(fct_entry)
                try:
                    resp = walletd.new_entry(factomd, chain_id, 
                                             [ 'TwitterBank Record',user_id, tweet_id ,public, signature],
                                             str(fct_entry), ec_address=ec_address) # makes entry into the factom testnet
                    
                    print(' Tweet Successfully Entered Into the Factom Testnet!')
                    print(resp)
                except exceptions.FactomAPIError as e:
                    print(e.data)
                
            except BaseException as e:
                print("Error on_data %s" % str(e))
                return True
      
        def on_error(self, status_code):
            print >> sys.stderr, 'Encountered error with status code:', status_code
            return True # Don't kill the stream
            print ("Stream restarted")

        def on_timeout(self):
            print >> sys.stderr, 'Timeout...'
            return True # Don't kill the stream
            print ("Stream restarted")