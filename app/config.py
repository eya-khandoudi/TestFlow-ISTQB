import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'testflow-istqb-secret-key-2026')
    DATABASE = os.environ.get('DATABASE', str(BASE_DIR / 'testflow.db'))
    TESTING = False
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    DATABASE = ':memory:'
    DEBUG = False
