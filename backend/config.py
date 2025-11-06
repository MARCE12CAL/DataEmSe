import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).parent
    
    # Directorios
    DATA_DIR = BASE_DIR / 'app' / 'data'
    PROFILES_DIR = DATA_DIR / 'profiles'
    BATCH_JOBS_DIR = DATA_DIR / 'batch_jobs'
    COMPARISON_REPORTS_DIR = DATA_DIR / 'comparison_reports'
    UPLOADS_DIR = BASE_DIR / 'uploads'
    TEMP_MUESTRAS_DIR = BASE_DIR / 'temp_muestras'
    OUTPUTS_DIR = BASE_DIR / 'outputs'
    
    for directory in [DATA_DIR, PROFILES_DIR, BATCH_JOBS_DIR, 
                     COMPARISON_REPORTS_DIR, UPLOADS_DIR, 
                     TEMP_MUESTRAS_DIR, OUTPUTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}