import os
from dotenv import load_dotenv

load_dotenv()

class Local(object):
   DEBUG = False if os.getenv("APP_ENV") == "production" else True 
   SECRET_KEY = os.getenv("SECRET_KEY", "dev")

   JWT_ACCESS_TOKEN_EXPIRES = 30*86400

   SQLALCHEMY_DATABASE_URI=os.getenv("DB_URL")
   SQLALCHEMY_TRACK_MODIFICATIONS=False

   TELEGRAM_SECRET = os.getenv("TELEGRAM_SECRET")

   WEB_BASE_URL = os.getenv("WEB_BASE_URL")