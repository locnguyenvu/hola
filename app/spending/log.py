import re
from sqlalchemy import and_

from app import exceptions
from app.di import get_db
import app.spending.category as spendingcategory

db = get_db()


TRANSACTION_TYPE_CREDIT = "credit"
TRANSACTION_TYPE_DEBIT = "debit"

class Log(db.Model):
    __tablename__ = "spending_log"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
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
    
    def set_amount_str(self, amount:str):
        if re.search(r"k$") != None:
            main = amount[0:amount.index("k")]


def find(filters):
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

    return query.all()

def find_id(id:int) -> Log:
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

def parse_chat_content(content:str) -> Log:
    
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

    return sl
