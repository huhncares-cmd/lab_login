import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_USER') or 'sqlite:///app.db'
    SECRET_KEY = os.environ.get('SECRET_KEY')