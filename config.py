import os

PASSWORD=os.environ['APP_PASSWORD']

class BaseConfig(object):
    DEBUG=False
    SECRET_KEY=os.environ['APP_SECRET_KEY']

class DevelopmentConfig(BaseConfig):
    DEBUG=True

class ProductionConfig(BaseConfig):
    DEBUG=False
