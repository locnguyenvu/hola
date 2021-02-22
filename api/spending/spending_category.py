from ..db import db, get_db_session
from .. import exceptions
from datetime import datetime

class SpendingCategory(db.Model):
    __tablename__ = "spending_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "created_at": self.created_at
        }

    def save(self):
        db_session = get_db_session()
        db_session.add(self)
        db_session.commit()

def get_all_spending_category() -> list:
    row_set = SpendingCategory.query.all()
    return list(map(lambda e: e.to_dict(), row_set))

def delete_spending_category(category_id) -> bool:
    category = SpendingCategory.query.filter_by(id=category_id).first()
    if category is None:
        return False
    db_session = get_db_session()
    db_session.delete(category)
    db_session.commit()
    return True

def create_spending_category(name, display_name=None):
    existed = SpendingCategory.query.filter_by(name=name).all()
    if len(existed) > 0:
        raise exceptions.ClientException(f"Category name *{name}* has existed")
    category = SpendingCategory(name=name, display_name=display_name, created_at=datetime.now(), updated_at=datetime.now())
    category.save()
    return category.to_dict()

def update_spending_category(category_id, **kwargs):
    category = SpendingCategory.query.filter_by(id=category_id).first()
    if category is None:
        raise exceptions.ClientException(f"Category not exists")
    if kwargs.get("display_name") is not None:
        category.display_name = kwargs.get("display_name")
    category.save()
    return True