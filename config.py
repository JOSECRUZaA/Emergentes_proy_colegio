import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración general"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    # Si estamos en Vercel (read-only filesystem), usar /tmp
    if os.environ.get('VERCEL'):
        fallback_db = 'sqlite:////tmp/colegio.db'
    else:
        fallback_db = 'sqlite:///colegio.db'
        
    db_url = os.getenv('DATABASE_URL', fallback_db)
    # SQLAlchemy 1.4+ requires 'postgresql://' instead of 'postgres://'
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configuración de pruebas"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
