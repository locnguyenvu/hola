from flask_sqlalchemy import SQLAlchemy
from flask import g

def init_app(app):
    db = SQLAlchemy()
    db.init_app(app)
    g.db = db

def get_db():
    return g.db 

def get_db_session():
    return g.db.session

