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
    created_at = db.Column("created_at", db.DateTime, server_default="NOW()")

    def __init__(self, fund:Fund):
        self.fund_id = fund.id
        self.fund_code = fund.name_short

def create(model:FundNavPriceHistory):
    # Prevent duplication
    existed = FundNavPriceHistory.query \
            .where(FundNavPriceHistory.fund_id == model.fund_id) \
            .where(FundNavPriceHistory.fund_code == model.fund_code) \
            .where(FundNavPriceHistory.dealing_date == model.dealing_date) \
            .where(FundNavPriceHistory.price == model.price) \
            .first()
    if existed != None:
        return

    if model.created_at is None:
        model.created_at = datetime.now()
    db.session.add(model)
    db.session.commit()