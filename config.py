from os import environ, path, urandom
from dotenv import load_dotenv
import base64



basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

password = environ.get('PASSWORD')
postgres_role = environ.get('ROLE_NAME')
database_name = 'music_history'


class BaseConfig(object):
    '''
    Base config class
    '''   
    key = base64.urlsafe_b64encode(urandom(32)).decode('utf-8')  # 32 bytes (256 bits) key
    environ["SECRET_KEY"] = key     
    
    DEBUG = True
    TESTING = False
    SECRET_KEY = key
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
