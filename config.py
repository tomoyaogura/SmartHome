import os

PULSE = 183
CODESEND_DIR = '/var/www/rfoutlet/codesend'
CODES = {"302-1": (4543795, 4543804),
         "302-2": (4543939, 4543948),
         "302-3": (4544259, 4544268),
         "302-4": (4545795, 4545804),
         "302-5": (4551939, 4551948)}
FILE_PATH =  os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'smarthome.db'

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(FILE_PATH, DB_NAME) 


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(FILE_PATH, 'test_db.db') 
    DEBUG = True

class DeploymentConfig(Config):
    """Configurations for Deployment."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'deployment': DeploymentConfig,
}
