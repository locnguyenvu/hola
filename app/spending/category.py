from datetime import datetime

from app import exceptions
from app.di import get_db

db = get_db()

class Category(db.Model):
    __tablename__ = "spending_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

def find_id(category_id):
    return Category.query.filter_by(id=category_id).first()

def find(filters) -> list:
    query = Category.query
    for attr in filters:
        if filters[attr] is None or not hasattr(Category, attr):
            continue
        query = query.filter(getattr(Category, attr)==filters[attr])
    return query.all()

def delete(category_id) -> bool:
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return False
    db.session.delete(category)
    db.session.commit()
    return True

def create(name, display_name=None):
    existed = Category.query.filter_by(name=name).all()
    if len(existed) > 0:
        raise exceptions.ClientException(f"Category name *{name}* has existed")
    category = Category(name=name, display_name=display_name, created_at=datetime.now(), updated_at=datetime.now())
    category.save()
    return category

def edit(category_id, payload):
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        raise exceptions.ClientException(f"Category not exists")
    for attr in payload:
        if payload[attr] is None or not hasattr(category, attr):
            continue
        setattr(category, attr, payload[attr])
    category.save()
    return True