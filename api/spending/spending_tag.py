from ..db import db, get_db_session
from .. import exceptions
from datetime import datetime

class SpendingTag(db.Model):
    __tablename__ = "spending_tag"

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.tag_name,
            "created_at": self.created_at
        }

    def save(self):
        db_session = get_db_session()
        db_session.add(self)
        db_session.commit()

class SpendingLogTag(db.Model):
    __tablename__ = 'spending_log_tag'

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, nullable=False)
    tag_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db_session = get_db_session()
        db_session.add(self)
        db_session.commit()

def get_all_spending_tag() -> list:
    row_set = SpendingTag.query.all()
    return row_set

def create_spending_tag(tag_name):
    existed = SpendingTag.query.filter_by(tag_name=tag_name).all()
    if (len(existed) > 0):
        raise exceptions.ClientException(f"Tag name *{tag_name}* has existed")
    model = SpendingTag(tag_name=tag_name)
    model.save()
    return True

def bulk_tag_logs(tag_id, log_ids):
    tag = SpendingTag.query.filter_by(id=tag_id).first()
    if (tag is None):
        raise exceptions.ClientException(f"Tag id #{tag_id} does not exist")
    for log_id in log_ids:
        tagMapping = SpendingLogTag(tag_id=tag.id, log_id=log_id)
        tagMapping.save()
