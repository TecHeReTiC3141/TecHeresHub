import random
import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'AlchDataBase.db') + '?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE = "TecHeresHub/tmp/sql/AlchDataBase.db"
    DEBUG = True
    SECRET_KEY = hex(random.randint(1000000, 10000000000000000))