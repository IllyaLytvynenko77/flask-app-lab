import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-flask-wtf-key-2026')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Максимальний розмір файлу: 2 МБ
    WTF_CSRF_ENABLED = True
