import re
from datetime import datetime
from sqlalchemy import and_

from app import exceptions
from app.di import get_db
from app.util import strings
import app.spending.category as spendingcategory

db = get_db()

TRANSACTION_TYPE_CREDIT = "credit"
TRANSACTION_TYPE_DEBIT = "debit"

class Log(db.Model):
    __tablename__ = "spending_log"

    id = db.Column(db.Integer, primary_key=True)
    telegram_message_id = db.Column(db.Integer, nullable=True)
    telegram_chat_id = db.Column(db.String, nullable=True)
    created_by = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    spending_category_id = db.Column(db.Integer, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def category_name(self):
        lcat = spendingcategory.find_id(self.spending_category_id)
        if lcat is not None:
            return lcat.display_name
        return None
    
    def set_amount_by_string(self, amount:str):
        self.amount = strings.toint_sipostfix(amount)

    def is_debit(self) -> bool:
        return self.transaction_type == TRANSACTION_TYPE_DEBIT

    def is_credit(self) -> bool:
        return self.transaction_type == TRANSACTION_TYPE_CREDIT



def find(filters, order_by_column=None, order_type="asc"):
    query = Log.query
    if 'from_date' in filters and 'to_date' in filters:
        query = query.filter(and_(
            Log.created_at >= filters['from_date'],
            Log.created_at <= filters['to_date']
        ))
        del filters['from_date']
        del filters['to_date']
    
    for condition in filters:
        if not hasattr(Log, condition) or filters[condition] == None or filters[condition] == '':
            continue
        query = query.filter(getattr(Log, condition)==filters[condition])
    
    if order_by_column is not None:
        if order_type == "asc":
            query = query.order_by(getattr(Log, order_by_column).asc())
        elif order_type == "desc":
            query = query.order_by(getattr(Log, order_by_column).desc())

    return query.all()

def find_id(id) -> Log:
    return Log.query.filter_by(id=id).first()


def edit(id:int, payloads):
    slog = Log.query.filter_by(id=id).first()
    if slog is None:
        raise exceptions.ClientException(f"#{id} does not existed")
    for attr in payloads:
        if not hasattr(slog, attr) or payloads[attr] is None or attr == 'id':
            continue
        if attr == 'spending_category_id' and spendingcategory.find_id(payloads[attr]) is None:
            raise exceptions.ClientException(f"Category id #{payloads[attr]} does not existed")
            
        setattr(slog, attr, payloads[attr])
    slog.save()

def new_from_chat_content(content:str) -> Log:
    
    msg_chunks = content.split(" ")
    amount = None
    for word in msg_chunks:
        amount_match = re.search(r"^\d+kc*", word)
        if amount_match is None:
            continue
        else:
            amount = amount_match[0]

    if amount is None:
        raise ValueError("Invalid chat message, spending amount not found")

    if amount in msg_chunks:
        msg_chunks.remove(amount)

    sl = Log()
    sl.subject = " ".join(msg_chunks)
    sl.transaction_type = TRANSACTION_TYPE_DEBIT
    if re.search(r"c$", amount):
        sl.transaction_type = TRANSACTION_TYPE_CREDIT
        amount = amount.rstrip("c")
    sl.set_amount_by_string(amount)
    sl.created_at = datetime.now()

    return sl

def save(model: Log):
    if model.created_at is None:
        model.created_at = datetime.now()
    model.updated_at = datetime.now()
    db.session.add(model)
    db.session.commit()