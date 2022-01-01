from flask import g
from telegram import Bot

def init_app(app):
    bot = Bot(app.config["TELEGRAM_SECRET"]) 
    g.telegram_bot = bot

def get_bot():
    return g.telegram_bot

