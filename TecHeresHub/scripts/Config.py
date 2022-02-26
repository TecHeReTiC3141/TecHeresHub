import random
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "TecHeresHub/tmp/sql/users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE = "TecHeresHub/tmp/sql/users.db"
    DEBUG = True
    SECRET_KEY = hex(random.randint(1000000, 10000000000000000))