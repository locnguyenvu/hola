from ..db import get_db
from .. import exceptions
from datetime import datetime

db = get_db()

class SpendingCategory(db.Model):
    __tablename__ = "spending_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()


def find(filters) -> list:
    query = SpendingCategory.query
    for attr in filters:
        if filters[attr] is None or not hasattr(SpendingCategory, attr):
            continue
        query = query.filter(getattr(SpendingCategory, attr)==filters[attr])
    return query.all()

def find_id(category_id):
    return SpendingCategory.query.filter_by(id=category_id).first()

def delete(category_id) -> bool:
    category = SpendingCategory.query.filter_by(id=category_id).first()
    if category is None:
        return False
    db.session.delete(category)
    db.session.commit()
    return True

def create(name, display_name=None):
    existed = SpendingCategory.query.filter_by(name=name).all()
    if len(existed) > 0:
        raise exceptions.ClientException(f"Category name *{name}* has existed")
    category = SpendingCategory(name=name, display_name=display_name, created_at=datetime.now(), updated_at=datetime.now())
    category.save()
    return category

def edit(category_id, payload):
    category = SpendingCategory.query.filter_by(id=category_id).first()
    if category is None:
        raise exceptions.ClientException(f"Category not exists")
    for attr in payload:
        if payload[attr] is None or not hasattr(category, attr):
            continue
        setattr(category, attr, payload[attr])
    category.save()
    return True
