from email.policy import default
from app.di import get_db

db = get_db()

DCVFM = "dcvfm"

class Fund(db.Model):

    __tablename__ = "investment_fund"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code = db.Column(db.String(100), unique=True, nullable=False)
    name_short = db.Column(db.String(200), unique=True, nullable=False)
    name_long = db.Column(db.String(255), unique=True, nullable=False)
    nav_price = db.Column(db.Float(10, 2), default=0.0)
    group = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


def list_dcfvm():
    query = Fund.query.filter_by(group=DCVFM)
    return query.all()
