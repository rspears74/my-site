import os

class BaseConfig(object):
    DEBUG=False
    SECRET_KEY=os.environ['APP_SECRET_KEY']
    PASSWORD=os.environ['APP_PASSWORD']

class DevelopmentConfig(BaseConfig):
    DEBUG=True

class ProductionConfig(BaseConfig):
    DEBUG=False
