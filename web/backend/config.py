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

    WALLET_BASE_URL = os.environ.get('WALLET_BASE_URL', 'http://18.222.184.135:8089')
    FACTOM_BASE_URL = os.environ.get('FACTOM_BASE_URL', 'http://18.222.184.135:8088')




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