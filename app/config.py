import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    STRIPE_API_KEY= os.environ.get('STRIPE_API_KEY')
    STRIPE_WEBHOOK_SECRET= os.environ.get('STRIPE_WEBHOOK_SECRET')