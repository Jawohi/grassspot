import os

class Config:
    # Grundlegende Konfigurationen, die für alle Umgebungen gelten
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    UPLOADED_PHOTOS_DEST = os.getenv('UPLOADED_PHOTOS_DEST')

class DevelopmentConfig(Config):
    # Entwicklungs-spezifische Konfigurationen
    DEBUG = True

class ProductionConfig(Config):
    # Produktions-spezifische Konfigurationen
    DEBUG = False

class TestingConfig(Config):
    # Test-spezifische Konfigurationen
    TESTING = True
