import random
import uuid

from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy import and_

from app.db import get_db

db = get_db()

STATE_NEW = "new"
STATE_ACTIVE = "active"
STATE_EXPIRED = "expired"
STATE_ABANDONED = "abandoned"
STATE_TERMINATED = "terminated"

class LoginSession(db.Model):
    __tablename__ = "login_session"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    session_name = db.Column(db.String, nullable=False)
    otp = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    expired_at = db.Column(db.DateTime, nullable=True)
    invalid_at = db.Column(db.DateTime, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def abandon(self):
        self.state = STATE_ABANDONED
        self.save()

    def activate(self):
        self.state = STATE_ACTIVE
        self.expired_at = datetime.now() + timedelta(seconds=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])
        self.otp = "**{}".format(self.otp[2:4])
        self.save()

    def terminate(self):
        self.state = STATE_TERMINATED
        self.save()

    def is_expired(self) -> bool:
        if self.state == STATE_ACTIVE:
            return datetime.now() >= self.expired_at
        return False


def new_login_session(user_id:int) -> LoginSession:
    code = uuid.uuid4()
    ttl = datetime.now() + timedelta(seconds=5*60)
    otp = random.randint(100000, 999999)
    session = LoginSession(
        user_id = user_id,
        session_name = str(code),
        state = STATE_NEW,
        otp = otp,
        created_at = datetime.now(),
        invalid_at = ttl,
    )
    session.save()
    return session

def find_session_by_name(name:str) -> LoginSession:
    query = LoginSession.query.filter(and_(
        LoginSession.session_name == name,
        LoginSession.invalid_at >= datetime.now(),
        LoginSession.state == STATE_NEW
    ))
    return query.first()

def abandon_session_invalid(user_id:int):
    invalid_sessions = LoginSession.query.filter(and_(
        LoginSession.user_id == user_id,
        LoginSession.state == STATE_NEW,
        LoginSession.invalid_at < datetime.now()
    )).all()
    for sess in invalid_sessions:
        sess.abandon()
    return

def terminate_session(name:str):
    sess = LoginSession.query.filter_by(session_name=name).first()
    sess.terminate()

def is_session_expired(name:str) -> bool:
    sess = LoginSession.query.filter_by(session_name=name).first()
    if sess is None:
        return False
    return sess.is_expired()
