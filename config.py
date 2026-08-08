import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Echoing every statement to stdout costs a measurable amount of request
    # time; opt in with SQLALCHEMY_ECHO=1 when debugging a query.
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', '').lower() in ('1', 'true', 'yes')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'cricketiq')
    
    # Build SQLAlchemy URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cricketiq.db'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    
    if MYSQL_PASSWORD:
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    else:
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
