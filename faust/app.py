import os
import asyncio
import logging
import json
from datetime import datetime
from hashlib import sha256

import time
import tweepy
import faust

from factom import Factomd, FactomWalletd

from factom.exceptions import FactomAPIError
from config import config
from decorators import sleep

conf = config[os.environ.get('SCRIBE_CONFIG', 'development')]
factom_url = conf.FACTOM_BASE_URL
wallet_url = conf.WALLET_BASE_URL
ec_address = conf.EC_ADDR
fct_address = conf.FC_ADDR

app = faust.App('Scribe', broker="kafka://localhost:9092")

class TwitterAccount(faust.Record, serializer='json'):
    handle: str
    twitterid: str
    chainid: str
    tracking: str

# source_topic = app.topic('Scribe', value_serializer='json')
source_topic = app.topic('Scribe', value_type=TwitterAccount)
@app.agent(source_topic)
async def process_tweets(twitter_accounts):
    factomd = Factomd(host=factom_url, ec_address=ec_address, fct_address=fct_address, username='rpc_username',password='rpc_password')
    walletd = FactomWalletd(host=wallet_url, ec_address=ec_address, fct_address=fct_address, username='rpc_username',password='rpc_password')
    async for twitter_account in twitter_accounts:
        print('TESTING NOW!')
        print(twitter_account)
        print(twitter_account.chainid)
        chainid = str(twitter_account.chainid)
        print(chainid)
        chain_id = check_chain(factomd, chainid)
        print(chain_id)
           

@sleep(5)       
def check_chain(factomd, chain_id):
    print('Checking Chain')
    try:
        print('Checkign Chain')
        chainhead =  factomd.chain_head(chain_id)
        print(chainhead)
        chain_id = chainhead['chainhead']
        logging.info('Retrieved chain: {} with corresponding id {} (double string)'.format(chain, chain_id))
        print(chain_id)
        return chain_id
    except KeyError as e:
        logging.debug('No chain found')
        return None

async def start_worker(worker: faust.Worker) -> None:
    """
    :param worker: A Faust worker instance that runs a certain app configuration. This
    consumes and partitions kafka queues based on specific topics
    :return: None
    """
    await worker.start()

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    worker = faust.Worker(app, loop=loop, loglevel='info')
    try:
#        loop.run_until_complete(producer())
        loop.run_until_complete(start_worker(worker))
    except KeyboardInterrupt:
        logging.info('Interrupted')
    finally:
        worker.stop_and_shutdown()
        logging.info('Cleaning up')
        loop.stop()