import os


class Config:
    SECRET_KEY = 'onixz-secret-key-2026'

    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # Cambiamos "postgresql://" por "postgresql+psycopg://" para usar la librería nueva
        db_url = db_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///onixz.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USER = 'admin'
    ADMIN_PASS = 'onixz'