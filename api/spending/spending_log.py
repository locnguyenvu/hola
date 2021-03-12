from .. import exceptions
from ..db import db, get_db_session 
from .spending_method import find_spending_method_by_id
from sqlalchemy import and_
from datetime import datetime

class SpendingLog(db.Model):
    __tablename__ = "spending_log"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    

    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "amount": self.amount,
            "created_at": self.created_at
        }

    def save(self):
        db_session = get_db_session()
        db_session.add(self)
        db_session.save()

def get_spending_log(from_date:datetime, to_date:datetime):
    return SpendingLog.query.filter(and_(
        SpendingLog.created_at >= from_date,
        SpendingLog.created_at <= to_date
    )).all()

def find_spending_log(id:int) -> SpendingLog:
    return SpendingLog.query.filter_by(id=id).first()

def update_spending_log(id:int, subject:str = None, amount:float = None, payment_method_id:int = None):
    slog = SpendingLog.query.filter_by(id=id).first()
    if slog is None:
        raise exceptions.ClientException(f"#{id} does not existed")
    if subject is not None:
        slog.subject = subject
    if amount is not None:
        slog.amount = amount
    if payment_method_id is not None:
        pmethod = find_spending_method_by_id(payment_method_id)
        if pmethod is None:
            raise exceptions.ClientException("Invalid payment method")
        slog.payment_method = pmethod.name
        slog.transaction_type = pmethod.type
    slog.save()
