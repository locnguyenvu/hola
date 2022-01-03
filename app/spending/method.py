from sqlalchemy import or_

from app import exceptions
from app.di import get_db

db = get_db()

class Method(db.Model):
    TYPE_DEBIT = "debit"
    TYPE_CREDIT = "credit"

    __tablename__ = "spending_method"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    alias = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime)

    def save(self):
        db.session.add(self)
        db.session.commit()

def create(name:str, type:str, alias:str = None) :
    if type not in [Method.TYPE_CREDIT, Method.TYPE_DEBIT]:
        raise exceptions.ClientException("Invalid spending method type")
    method = Method(
        name=name,
        type=type,
        alias=alias
    )
    method.save()
    return method

def find(filters):
    query = Method.query
    for attr in filters:
        if not hasattr(Method, attr) or filters[attr] is None:
            continue
        query = query.filter(getattr(Method, attr)==filters[attr])
    return query.all()

def find_id(id:int) -> Method:
    return Method.query.filter_by(id=id).first()

def find_fuzzy(payment_method:str) -> Method:
    method = Method.query.filter(or_(
        Method.alias == payment_method,
        Method.name == payment_method 
    )).first()
    return method
