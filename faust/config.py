""" This module provides configuration for the flask apps in different environments"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    KAFKA_URL = os.environ.get('KAFKA_URL', 'kafka://localhost:9092')
    FC_ADDR = os.environ.get('FC_ADDR', 'FA3qdHM7pH5JDw6EaM9x5vxRtsRSy16xCEMhaJDSmECUgZQy9ob3')
    EC_ADDR = os.environ.get('EC_ADDR', 'EC34ywXCgXE4qA3Pr52QzCfnXptKXySeYr3QcPNgqWZLyNRckgrq')

    RPC_USER = os.environ.get('RPC_USER', None)
    RPC_PASS = os.environ.get('RPC_PASS', None)

    WALLET_BASE_URL = os.environ.get('WALLET_BASE_URL', 'http://13.59.114.88:8089')
    FACTOM_BASE_URL = os.environ.get('FACTOM_BASE_URL', 'http://13.59.114.88:8088')

    TWITTER_KEY = os.environ.get('TWITTER_KEY', '8OkElZxTSOxPTHRzMxlkY0F5E')
    TWITTER_SECRET = os.environ.get('TWITTER_SECRET', 'CVFmGkBkwchWhjRdDY6x3gOWxouhP6z4ohpgNlqgSdx1QUzYJz')
    TWITTER_APP_KEY = os.environ.get('TWITTER_APP_KEY', '1088516191436656640-if27Ij2ssb3PWI5g5USIKi1BOtN08I')
    TWITTER_APP_SECRET = os.environ.get('TWITTER_APP_SECRET', 'u4VmQZ256FTT5IrwEpErUeLr2Ta8W9CJJdgEpa5uznj2H')





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