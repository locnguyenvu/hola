import re
from flask import Blueprint, make_response
from flask_jwt_extended import jwt_required

from .db import get_db

db = get_db()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    telegram_username = db.Column(db.String, nullable=False)
    telegram_userid = db.Column(db.Integer, nullable=False)
    session_alias = db.Column(db.String, nullable=True)
    pin = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Integer, nullable=False)


    @classmethod
    def find_by_telegram_account(cls, account_identity):
        if re.match(r"^\-*\d+$", account_identity):
            row = cls.query.filter_by(telegram_userid=account_identity).first()
        else:
            row = cls.query.filter_by(telegram_username=account_identity).first()
        return row

    @classmethod
    def clear_session(cls, session_alias):
        record = cls.query.filter_by(session_alias=session_alias).first()
        if record is not None:
            record.session_allias = None
            db.session.add(record)
            db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

def find_by_telegram_account(account_identity):
    if re.match(r"^\-*\d+$", account_identity):
        row = User.query.filter_by(telegram_userid=account_identity).first()
    else:
        row = User.query.filter_by(telegram_username=account_identity).first()
    return row

def find_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


bp = Blueprint('user', __name__)

@bp.route("/user")
@jwt_required()
def index():
    data = list(map(lambda e: {
        "id": e.id,
        "telegram_username": e.telegram_username,
        "is_active": e.is_active
    }, User.query.all()))
    return make_response({
        "data": data
    })


