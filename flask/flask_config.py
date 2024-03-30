import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Config(object):
    pass

class devConfig(Config):
    pass

class prodConfig(Config):
    pass