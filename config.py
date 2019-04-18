import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'database_lab5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://book_management_system_user:test_password@localhost:3306/book_management_system_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    