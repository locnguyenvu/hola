from api.spending.spending_category import SpendingCategory
from sqlalchemy import and_
from datetime import datetime

from .. import exceptions
from ..db import db, get_db_session 
from .spending_category import find_id as category_find_id

class SpendingLog(db.Model):
    __tablename__ = "spending_log"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    spending_category_id = db.Column(db.Integer, nullable=True)
    
    def save(self):
        db_session = get_db_session()
        db_session.add(self)
        db_session.commit()

    @property
    def category_name(self):
        category = category_find_id(self.spending_category_id)
        if category is not None:
            return category.display_name
        return None

        

def find(filters):
    query = SpendingLog.query
    if 'from_date' in filters and 'to_date' in filters:
        query = query.filter(and_(
            SpendingLog.created_at >= filters['from_date'],
            SpendingLog.created_at <= filters['to_date']
        ))
        del filters['from_date']
        del filters['to_date']
    
    for condition in filters:
        if not hasattr(SpendingLog, condition) or filters[condition] is None:
            continue
        query = query.filter(getattr(SpendingLog, condition)==filters[condition])

    return query.all()

def find_id(id:int) -> SpendingLog:
    return SpendingLog.query.filter_by(id=id).first()


def edit(id:int, payloads):
    slog = SpendingLog.query.filter_by(id=id).first()
    if slog is None:
        raise exceptions.ClientException(f"#{id} does not existed")
    for attr in payloads:
        if not hasattr(slog, attr) or payloads[attr] is None or attr == 'id':
            continue
        if attr == 'spending_category_id' and category_find_id(payloads[attr]) is None:
            raise exceptions.ClientException(f"Category id #{payloads[attr]} does not existed")
            
        setattr(slog, attr, payloads[attr])
    slog.save()