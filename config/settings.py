"""
Configuration Settings
SIH PS1 - Cybersecurity Threat Detector
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
MODELS_DIR = DATA_DIR / 'models'
LOGS_DIR = PROJECT_ROOT / 'logs'

# Flask settings
FLASK_CONFIG = {
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'sih-ps1-secret-key')
}

# Threat detection settings
DETECTION_CONFIG = {
    'RISK_THRESHOLD': 0.5,
    'CONFIDENCE_THRESHOLD': 0.6,
    'MAX_TEXT_LENGTH': 10000,
    'ANALYSIS_TIMEOUT': 30
}

# API settings
API_CONFIG = {
    'RATE_LIMIT': '100/hour',
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB
    'ALLOWED_EXTENSIONS': {'txt', 'json', 'csv'}
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
