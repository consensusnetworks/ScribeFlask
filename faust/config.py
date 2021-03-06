""" This module provides configuration for the flask apps in different environments"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    KAFKA_URL = os.environ.get('KAFKA_URL', 'kafka://localhost:9092')
    FC_ADDR = os.environ.get('FC_ADDR', 'YourFCAddress')
    EC_ADDR = os.environ.get('EC_ADDR', 'YourECADDRESS')

    RPC_USER = os.environ.get('RPC_USER', None)
    RPC_PASS = os.environ.get('RPC_PASS', None)

    WALLET_BASE_URL = os.environ.get('WALLET_BASE_URL', 'http://YourHost:8089')
    FACTOM_BASE_URL = os.environ.get('FACTOM_BASE_URL', 'http://YourHost:8088')

    TWITTER_KEY = os.environ.get('TWITTER_KEY', 'Your_Twitter_Key')
    TWITTER_SECRET = os.environ.get('TWITTER_SECRET', 'Your_Twitter_Secret')
    TWITTER_APP_KEY = os.environ.get('TWITTER_APP_KEY', 'Your_Twitter_App_Key')
    TWITTER_APP_SECRET = os.environ.get('TWITTER_APP_SECRET', 'Your_Twitter_App_Secret')





class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}