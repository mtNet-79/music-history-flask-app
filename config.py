from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

password = environ.get('PASSWORD')
postgres_role = environ.get('ROLE_NAME')
database_name = 'music_history'


class BaseConfig(object):
    '''
    Base config class
    '''   
    
    DEBUG = True
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY')
    database_path = 'postgresql://{}:{}@{}/{}'.format(
        postgres_role, password, 'localhost:5432', database_name)
    SQLALCHEMY_DATABASE_URI = database_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(BaseConfig):
    """Set Flask config variables."""

    FLASK_ENV = 'development'


class TestingConfig(BaseConfig):
    
    database_path = 'postgresql://{}:{}@{}/{}'.format(
        postgres_role, password, 'localhost:5432', 'music_history_test')
    SQLALCHEMY_DATABASE_URI = database_path
    TESTING = True
