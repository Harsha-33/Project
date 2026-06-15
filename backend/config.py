import os
from datetime import timedelta
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

load_dotenv()


def _database_url():
    url = os.getenv('DATABASE_URL')
    allow_sqlite = os.getenv('ALLOW_SQLITE_FALLBACK', 'false').lower() == 'true'

    if not url:
        if allow_sqlite:
            return 'sqlite:///wecareforyou.db'
        raise RuntimeError('DATABASE_URL is required. Set it to the Supabase PostgreSQL URL in backend/.env.')

    if url.startswith('postgresql://') and 'sslmode=' not in url:
        parsed = urlsplit(url)
        query = dict(parse_qsl(parsed.query))
        query['sslmode'] = 'require'
        url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))

    return url


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    DATABASE_URL = _database_url()
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': NullPool,
        'pool_pre_ping': True
    }

    LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'application.log')
