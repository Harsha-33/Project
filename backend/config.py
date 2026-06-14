import os
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    DATABASE_URL = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///wecareforyou.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': NullPool,
        'pool_pre_ping': True
    }

    LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'application.log')
