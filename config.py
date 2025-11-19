"""
在庫管理システム - 環境設定
config.py
"""
import os
from datetime import timedelta


class Config:
    """基本設定"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # セキュリティ設定
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_SSL_STRICT = True
    
    # アップロード設定
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'xlsx', 'csv'}
    
    # ページネーション
    ITEMS_PER_PAGE = 50
    HISTORY_PER_PAGE = 100
    
    # キャッシュ
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # メール設定（本番用）
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Redis (本番環境)
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # レート制限
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    
    # ログ
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///inventory_dev.db'
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_SSL_STRICT = False


class ProductionConfig(Config):
    """本番環境設定"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/inventory_prod'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }


class TestingConfig(Config):
    """テスト環境設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}