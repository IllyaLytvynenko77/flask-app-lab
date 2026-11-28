import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-lab8")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", "False").lower() == "true"
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
