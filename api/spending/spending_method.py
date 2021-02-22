from api.spending import spending_category
from ..db import db, get_db_session
from .. import exceptions
from sqlalchemy import or_

class SpendingMethod(db.Model):
    TYPE_DEBIT = "debit"
    TYPE_CREDIT = "credit"

    __tablename__ = "spending_method"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    alias = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "alias": self.alias,
            "type": self.type
        }

    def save(self):
        db_session = get_db_session()
        db_session.add(self)
        db_session.commit()

def create_spending_method(name:str, type:str, alias:str = None) -> dict:
    if type not in [SpendingMethod.TYPE_CREDIT, SpendingMethod.TYPE_DEBIT]:
        raise exceptions.ClientException("Invalid spending method type")
    method = SpendingMethod(
        name=name,
        type=type,
        alias=alias
    )
    method.save()
    return method.to_dict()

def get_spending_methods():
    methods = SpendingMethod.query.all()
    return list(map(lambda e: e.to_dict(), methods))

def find_spending_method_by_id(id:int) -> SpendingMethod:
    return SpendingMethod.query.filter_by(id=id).first()

def find_spending_method(payment_method:str) -> SpendingMethod:
    method = SpendingMethod.query.filter(or_(
        SpendingMethod.alias == payment_method,
        SpendingMethod.name == spending_category
    )).first()
    return method
