import app.spending.log as spendinglog

from app import exceptions
from app.di import get_db

db = get_db()

class Tag(db.Model):
    __tablename__ = "spending_tag"

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Integer, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

class LogTag(db.Model):
    __tablename__ = 'spending_log_tag'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('spending_tag.id'))
    log_id = db.Column(db.Integer, db.ForeignKey('spending_log.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

def get_all_spending_tag() -> list:
    row_set = Tag.query.all()
    return row_set

def create_spending_tag(tag_name):
    existed = Tag.query.filter_by(tag_name=tag_name).all()
    if (len(existed) > 0):
        raise exceptions.ClientException(f"Tag name *{tag_name}* has existed")
    model = Tag(tag_name=tag_name)
    model.save()
    return True

def edit_spending_tag(id, params):
    tag = Tag.query.filter_by(id=id).first()
    if (tag is None):
        raise exceptions.ClientException(f"Tag with id #{id} does not exist")
    for attr in params:
        if (hasattr(tag, attr)):
            setattr(tag, attr, params[attr])
    tag.save()

def bulk_tag_logs(tag_id, log_ids):
    tag = Tag.query.filter_by(id=tag_id).first()
    if (tag is None):
        raise exceptions.ClientException(f"Tag id #{tag_id} does not exist")
    for log_id in log_ids:
        tagMapping = LogTag(tag_id=tag.id, log_id=log_id)
        tagMapping.save()

def get_log_with_tag(tag_id):
    return spendinglog.Log.query.join(LogTag, LogTag.log_id==spendinglog.Log.id).filter(LogTag.tag_id==tag_id).all()
