from datetime import datetime

from app.di import get_db
from .fund import Fund

db = get_db()

class FundCertificateSubscription(db.Model):

    __tablename__ = "investment_fund_certificate_subscription"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    fund_id = db.Column("fund_id", db.Integer, nullable=False)
    fund_code = db.Column("fund_code", db.String, nullable=False)
    dealing_date = db.Column("dealing_date", db.Date, nullable=False)
    gross_subscription_amount = db.Column("gross_subscription_amount", db.Float(10, 2), nullable=False)
    actual_subscription_amount = db.Column("actual_subscription_amount", db.Float(10, 2), nullable=False)
    total_charges = db.Column("total_charges", db.Float(10, 2), nullable=False)
    net_subscription_amount = db.Column("net_subscription_amount", db.Float(10, 2), nullable=False)
    subscription_price = db.Column("subscription_price", db.Float(10, 2), nullable=False)
    quantity = db.Column("quantity", db.Float(10, 2), nullable=False)
    created_at = db.Column("created_at", db.DateTime)

    def __init__(self, fund:Fund):
        self.fund_id = fund.id
        self.fund_code = fund.name_short

def save(model:FundCertificateSubscription):
    # Prevent duplication
    existed = FundCertificateSubscription.query \
            .where( FundCertificateSubscription.fund_id == model.fund_id) \
            .where(FundCertificateSubscription.fund_code == model.fund_code) \
            .where(FundCertificateSubscription.dealing_date == model.dealing_date) \
            .where(FundCertificateSubscription.gross_subscription_amount == model.gross_subscription_amount) \
            .where(FundCertificateSubscription.quantity == model.quantity) \
            .first()
    if existed != None:
        return

    if model.created_at is None:
        model.created_at = datetime.now()
    db.session.add(model)
    db.session.commit()