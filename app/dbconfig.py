from datetime import datetime
from .di import get_db

db = get_db()

class DbConfig(db.Model):

    __tablename__ = "config"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

def load_dbconfig(app):
    records = DbConfig.query.all()
    for reco in records:
        app.config[reco.path] = reco.value

def get(key:str):
    return DbConfig.query.filter_by(path=key).first()

def get_bulk(keys:list) -> dict:
    resultset = DbConfig.query.filter(DbConfig.path.in_(keys)).all()
    configs = {}
    for row in resultset:
        configs[row.path] = row.value
    return configs

def set(key:str, value):
    config = DbConfig.query.filter_by(path=key).first()
    if not config:
        config = DbConfig()
        config.path = key
        config.created_at = datetime.now()

    config.value = value
    config.updated_at = datetime.now()
    db.session.add(config)
    db.session.commit()

