import random

class Config:
    DATABASE = "TecHeresHub/tmp/sql/users.db"
    DEBUG = True
    SECRET_KEY = hex(random.randint(1000000, 10000000000000000))