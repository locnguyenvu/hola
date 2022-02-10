from datetime import datetime
from app.di import get_db

from .fund import Fund

db = get_db()

class FundNavPriceHistory(db.Model):

    __tablename__ = "investment_fund_nav_price_history"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    fund_id = db.Column("fund_id", db.Integer, nullable=False)
    fund_code = db.Column("fund_code", db.String, nullable=False)
    update_date = db.Column("update_date", db.Date, nullable=False)
    dealing_date = db.Column("dealing_date", db.Date, nullable=False)
    price = db.Column("price", db.Numeric(10, 2), nullable=False)
    net_change = db.Column("net_change", db.Numeric(10, 2), nullable=False)
    probation_change = db.Column("probation_change", db.Numeric(10, 2), nullable=False)
    is_active = db.Column("is_active", db.Integer, default=0)
    created_at = db.Column("created_at", db.DateTime, server_default="NOW()")

    def __init__(self, fund:Fund):
        self.fund_id = fund.id
        self.fund_code = fund.name_short

    def __str__(self) -> str:
        change_symbol = "▴"
        if self.net_change < 0:
            change_symbol = "▿"
        
        return "{:<6} {:>7,} ({}{}%)".format(self.fund_code.upper(), self.price, change_symbol, abs(self.probation_change))

def create(model:FundNavPriceHistory):
    if existed(model):
        return
    model.created_at = datetime.now()
    db.session.add(model)
    db.session.commit()

def existed(model:FundNavPriceHistory) -> bool:
    existed = FundNavPriceHistory.query \
            .where(FundNavPriceHistory.fund_id == model.fund_id) \
            .where(FundNavPriceHistory.fund_code == model.fund_code) \
            .where(FundNavPriceHistory.dealing_date == model.dealing_date) \
            .where(FundNavPriceHistory.price == model.price) \
            .first()
    return existed != None

def mark_active_price(fund:Fund):
    FundNavPriceHistory.query.filter_by(fund_id=fund.id, is_active=1).update({"is_active": 0})

    latest_price = FundNavPriceHistory.query.filter_by(fund_id=fund.id).order_by(FundNavPriceHistory.dealing_date.desc()).first()
    latest_price.is_active = 1
    fund.nav_price = latest_price.price
    fund.updated_at = datetime.now()

    db.session.add(latest_price)
    db.session.add(fund)
    db.session.commit()
