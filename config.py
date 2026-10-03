import os


class Config:
    SECRET_KEY = 'onixz-secret-key-2026'

    # Si existe DATABASE_URL (en Render, conectado a Neon), la usa.
    # Si no (en tu Codespace local), usa el SQLite de siempre.
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///onixz.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USER = 'admin'
    ADMIN_PASS = 'onixz'