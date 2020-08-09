import os

from hashlib import md5

class Dev:
    SECRET_KEY = 'YOUWILLNEVERGUESS'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bot_test.db'
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = md5('qwerty'.encode()).hexdigest()


class Prod:
    SECRET_KEY = os.getenv('TBOT_SECRETKEY', 'YOUWILLNEVERGUESS')
    SQLALCHEMY_DATABASE_URI = os.getenv('TBOT_DATABASE_URI', 'sqlite:///bot_prod.db')
    ADMIN_USERNAME = os.getenv('TBOT_ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = md5(os.getenv('TBOT_ADMIN_PASSWORD', 'qwerty').encode()).hexdigest()