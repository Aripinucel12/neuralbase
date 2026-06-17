import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-immediately')
    DATABASE = os.path.join(BASE_DIR, 'neuralbase.db')

    # Admin credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'change-me-immediately')

    # App
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = False
