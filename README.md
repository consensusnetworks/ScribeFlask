# ScribeFlask
## Introduction

Scribe is a software product that tracks any given number of twitter accounts and writes their tweets to the Factom Blockchain. You can track as many or as few accounts as you would like and the software will asynchronously spin up a Stream Listener to track the account and simultaneously scrape their roughly 3000 most recent tweets. These tweets are then written to the Factom Blockchain. Each twitter account being tracked has its own chain. This software utilizes Tweepy, Factom-API, and Robinhood Faust to perform its tasks.

## Prerequistes:

You will need to have docker and python installed in order to operate the software in its current form. Go here https://docs.docker.com/install/ for instructions on how to properly install docker. You will also need to isntall pipenv. To do so:
```
pip3 install pipenv
```

You will also need to register for Twitter Api keys at https://developer.twitter.com/, have an FCT and EC address to transact on the Factom Network, and a Factom node to operate the software. You will also need to manually insert these in the config.py files found within the faust and web folders.

## Running the software

To run the Flask API endpoint, database, and kafka server, from the main directory run:
```
docker-compose build
docker-compose up
```

To run the faust agent that will asynchronously gather an accounts most recent tweets, begin trackign them, and write them to the Factom blockchain, open a second terminal window and run the following after the kafka server has started:
```
pipenv run python faust/app.py
```

Currently you have to use postman to use the API. The frontend is currently being built.
