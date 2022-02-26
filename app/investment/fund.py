from calendar import month
from datetime import datetime
from turtle import update
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
    update_weekday = db.Column(db.String(7))

    def has_updated_today(self) -> bool:
        today = datetime.today()
        return today.year == self.updated_at.year \
            and today.month == self.updated_at.month \
            and today.day == self.updated_at.day


def list_dcfvm(update_today=True):
    query = Fund.query.filter_by(group=DCVFM)
    if update_today:
        today = datetime.today()
        weekday_index = ['_'] * 7
        weekday_index[today.weekday()] = "1"
        query = query.filter(Fund.update_weekday.like("".join(weekday_index)))

    return query.all()

def find_dcvfm_by_code(code:str):
    query = Fund.query \
            .where(Fund.group == DCVFM) \
            .where(Fund.name_short == code)
    return query.all()

def get_dcvfm_by_code(code:str) -> Fund:
    query = Fund.query \
            .where(Fund.group == DCVFM) \
            .where(Fund.name_short == code)
    return query.first()

def find_by_code(code:str) -> Fund:
    query = Fund.query.filter_by(name_short=code)
    return query.first()
