from .db import get_db

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
