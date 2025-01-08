import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'trudne-do-zgadniecia-haslo'
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('AZURE_SQL_CONNECTION_STRING')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Azure Storage
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_STORAGE_CONTAINER = 'photos'
    
    # Azure Service Bus
    AZURE_SERVICE_BUS_CONNECTION_STRING = os.environ.get('AZURE_SERVICE_BUS_CONNECTION_STRING')
    AZURE_QUEUE_NAME = 'photo-queue'
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Logging
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False