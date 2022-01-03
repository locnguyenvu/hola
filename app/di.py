from flask import g
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from telegram import Bot

def bootstrap(app):
    g.bot = Bot(app.config["TELEGRAM_SECRET"]) 
    g.jwt = JWTManager(app)
    g.db = SQLAlchemy(app)

def get_bot():
    return g.bot

def get_db():
    return g.db

def get_jwt():
    return g.jwt