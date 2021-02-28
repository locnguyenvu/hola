import os

class Local(object):
   DEBUG = False if os.getenv("APP_ENV") == "production" else True 
   SECRET_KEY = os.getenv("SECRET_KEY", "dev")

   JWT_ACCESS_TOKEN_EXPIRES = 30*86400

   SQLALCHEMY_DATABASE_URI=os.getenv("DB_URL")
   SQLALCHEMY_TRACK_MODIFICATIONS=False