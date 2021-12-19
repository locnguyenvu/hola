from sqlalchemy import or_
from ..db import get_db
from .. import exceptions

db = get_db()

class SpendingMethod(db.Model):
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
    if type not in [SpendingMethod.TYPE_CREDIT, SpendingMethod.TYPE_DEBIT]:
        raise exceptions.ClientException("Invalid spending method type")
    method = SpendingMethod(
        name=name,
        type=type,
        alias=alias
    )
    method.save()
    return method

def find(filters):
    query = SpendingMethod.query
    for attr in filters:
        if not hasattr(SpendingMethod, attr) or filters[attr] is None:
            continue
        query = query.filter(getattr(SpendingMethod, attr)==filters[attr])
    return query.all()

def find_id(id:int) -> SpendingMethod:
    return SpendingMethod.query.filter_by(id=id).first()

def find_fuzzy(payment_method:str) -> SpendingMethod:
    method = SpendingMethod.query.filter(or_(
        SpendingMethod.alias == payment_method,
        SpendingMethod.name == payment_method 
    )).first()
    return method
