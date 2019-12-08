# ScribeFlask
## Introduction

Scribe is a software product that tracks any given number of twitter accounts and writes their tweets to the Factom Blockchain. This project is refactored version of the original project that makes use of Flask as opposed to Django. The project, as is, is currently intended to utilize the Factom Testnet, but writing to the mainnet should be possible. You can track as many or as few accounts as you would like and the software will asynchronously spin up a Stream Listener to track the account and simultaneously scrape their roughly 3000 most recent tweets. These tweets are then written to the Factom Blockchain. Each twitter account being tracked has its own chain. Among the other libraries that this software utilizes are Tweepy, Factom-API, Kafka, and Robinhood Faust. More information on Kafka & Robinhood's Faust library for asynchronous kafka-stram processing in Python may be found https://kafka.apache.org/ && https://github.com/robinhood/faust respectively. In its current architecture, this software is comprised of a dockerized web application that allows you to natively track twitter accounts and a dockerized daemon that asynchronously handles all processing and writing tweets to Factom.

## Prerequistes:

You will need to have docker & docker-compose installed in order to operate the software. Go here https://docs.docker.com/install/ for instructions on how to properly install docker. 

You will also need to register for Twitter Api keys at https://developer.twitter.com/, have an FCT and EC address to transact on the Factom Network, and a Factom node to operate the software. You can find more information on how to get started setting up a Factom Node or and getting a wallet here: https://github.com/FactomProject/distribution. If you are operating this software with intention to utilize the testnet & need testnet Factoids to transact on the network, you can get some here: https://faucet.factoid.org/.

## Starting the Application

First Clone this directory:
```
git clone https://github.com/consensusnetworks/ScribeFlask
```
Within the web/backend folder and faust folders there are two files labeled config.py. You will need to open these files and insert your credentials, i.e Factom Addresses and Twitter API Keys. Now, simply navigate back to the main directory and run the following commands to build & start the application
```
docker-compose build
docker-compose up
```
Once the app is up and running, you should be able to access it at http://localhost:8001
## Starting the Daemon
To run faust agent that will asynchronously gather an accounts most recent tweets, begin trackign them, and write them to the Factom blockchain, open a second terminal window and run the following from the main directory after the application has been built and is running:
```
cd faust
docker build .
docker run -p 6066:6066 -p 9092:9092 --network=host <Container_ID>
```
**Note**: Make sure you change the container id to the one created at the end of the build.

## Using the Software
You will first be prompted to register, input the appropriate credentials and then do so again at login. Once inside the app, it is a very simple form-list structure that allows you to input an account's twitter handle and twitter id and press a button to start tracking them. If you need help finding an accounts twitter id use https://tweeterid.com/.

## Areas that still need improved:

1.) Fleshed out error handling throughout the application
2.) Incorporating a get API into the flask portion to load all accounts being tracked upon entry as they are only recorded to the UI currently and are deleted after a session expires.
3.) More robust way of loading credentials while maintaining security (is loading them into db fine, or do we need a more secure method?)
4.) Incorporating API or Daemon that will coordinate the efforts of all of the different Scribes to write to the same chain for the same accounts.
5.) Incorporating IDs for Scribes

