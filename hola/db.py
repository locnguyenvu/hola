from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


connection = SQLAlchemy()


def init_app(app: Flask):
    connection.init_app(app)


class ActiveRecord:
    def save(self):
        query = getattr(self, 'query')
        if hasattr(self, 'created_at') and getattr(self, 'created_at') is None:
            setattr(self, 'created_at', datetime.now())
        if hasattr(self, 'updated_at'):
            setattr(self, 'updated_at', datetime.now())
        query.session.add(self)
        query.session.commit()

    def is_new(self):
        if hasattr(self, 'id') and getattr(self, 'id') is None:
            return True
        return False
