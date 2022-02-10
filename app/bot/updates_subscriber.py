from datetime import datetime

import telegram

from app.di import get_db

db = get_db()

class UpdatesSubcriber(db.Model):

    __tablename__ = "bot_updates_subscriber"
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    topic = db.Column("topic", db.String, nullable=False)
    telegram_userid = db.Column("telegram_userid", db.Integer, nullable=False)
    created_at = db.Column("created_at", db.DateTime)

def save(model: UpdatesSubcriber):
    if UpdatesSubcriber.query.filter_by(topic=model.topic, telegram_userid=model.telegram_userid).first():
        raise ValueError("Duplicate on register")

    if not model.created_at:
        model.created_at = datetime.now()
    db.session.add(model)
    db.session.commit()

def delete(model: UpdatesSubcriber):
    db.session.delete(model)
    db.session.commit()

def get_subscribers(topic:str) -> list:
    return UpdatesSubcriber.query.filter_by(topic=topic).all()
