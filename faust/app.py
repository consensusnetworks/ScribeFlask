import os
import asyncio
import logging
import json
from datetime import datetime
from hashlib import sha256

import time
# import tweepy
import faust

from factom import Factomd, FactomWalletd
from config import config


conf = config[os.environ.get('CHAINSVC_CONFIG', 'development')]
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


chains = app.topic('Chains', value_serializer='json')
handles = app.topic('Handles', value_serializer='json')
tweetids = app.topic('TweetIDs', value_serializer='json')
# source_topic = app.topic('Scribe', value_serializer='json')

chainStream = app.stream(chains)
handleStream = app.stream(handles)
IDStream = app.stream(tweetids)

@app.task()
async for value in (chainStream & handleStream & IDStream):
    print(value)
# @app.agent(source_topic)
# async def process(stream):
#     async for payload in stream:
#         print('TESTING NOW!')
#         twitteraccount = json.loads(payload)
#         print(twitteraccount)

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