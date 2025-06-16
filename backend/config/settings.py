import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Application settings
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# API settings
API_PREFIX = '/api'
API_VERSION = 'v1'

# Model settings
MODEL_DIR = os.path.join(BASE_DIR, 'models')
DEFAULT_MODEL_PATH = os.path.join(MODEL_DIR, 'disease_model.joblib')

# NLP settings
NLP_SETTINGS = {
    'language': 'id',
    'min_token_length': 2,
    'max_tokens': 100
}

# Logging settings
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# Ensure required directories exist
for directory in [MODEL_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# CORS settings
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
CORS_METHODS = ['GET', 'POST', 'OPTIONS']
CORS_HEADERS = ['Content-Type', 'Authorization']

# Rate limiting
RATE_LIMIT = {
    'default': '100/hour',
    'predict': '50/hour',
    'chat': '200/hour'
}

# Cache settings
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300

# Security settings
SECURITY_SETTINGS = {
    'password_hash_algorithm': 'bcrypt',
    'token_expiration': 3600,  # 1 hour
    'max_login_attempts': 5,
    'lockout_time': 300  # 5 minutes
}

# Database settings (if needed in the future)
DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Email settings (if needed in the future)
EMAIL = {
    'host': os.getenv('EMAIL_HOST', 'smtp.gmail.com'),
    'port': int(os.getenv('EMAIL_PORT', 587)),
    'use_tls': True,
    'username': os.getenv('EMAIL_USERNAME', ''),
    'password': os.getenv('EMAIL_PASSWORD', '')
}

# Frontend settings
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# API Documentation settings
API_DOCS = {
    'title': 'Disease Detection API',
    'description': 'API for detecting diseases based on symptoms using NLP',
    'version': '1.0.0',
    'docs_url': '/docs',
    'redoc_url': '/redoc'
} 