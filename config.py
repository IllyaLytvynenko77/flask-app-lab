import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-for-your-project")
    VALID_USERNAME = os.environ.get("VALID_USERNAME", "admin")
    VALID_PASSWORD = os.environ.get("VALID_PASSWORD", "12345")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret-key"
