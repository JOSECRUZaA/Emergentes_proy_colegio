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
        
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', fallback_db)
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
