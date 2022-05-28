import os
from dotenv import load_dotenv

load_dotenv()


class Local(object):
    DEBUG = False if os.getenv("APP_ENV") == "production" else True
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    JWT_ACCESS_TOKEN_EXPIRES = 30 * 86400

    LOCALE = os.getenv("LOCALE", "vi_VN")

    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TELEGRAM_SECRET = os.getenv("TELEGRAM_SECRET")
    TELEGRAM_AUTH_CALLBACK = os.getenv("TELEGRAM_AUTH_CALLBACK")
    TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")

    WEB_BASE_URL = os.getenv("WEB_BASE_URL")
