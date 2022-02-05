from datetime import datetime

from app.di import get_db

db = get_db()

class Log(db.Model):

    __tablename__ = "income_log"


    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    subject = db.Column("subject", db.String, nullable=False)
    amount = db.Column("amount", db.Numeric(10,2), nullable=False)
    created_at = db.Column("created_at", db.DateTime, server_default="NOW()")
    updated_at = db.Column("updated_at", db.DateTime)


def save(model: Log):
    if not model.created_at:
        model.created_at = datetime.now()
    if not model.updated_at:
        model.updated_at = datetime.now()

    db.session.add(model)
    db.session.commit()

