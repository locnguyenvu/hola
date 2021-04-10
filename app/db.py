from flask_sqlalchemy import SQLAlchemy
from flask import g

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    g.db = db
    g.db_session = db.session

def get_db():
    return db

def get_db_session():
    return db.session