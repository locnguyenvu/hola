from datetime import datetime

from app.di import get_db
from app.investment.fund import Fund

db = get_db()

class FundCertificateRedemption(db.Model):

    __tablename__ = "investment_fund_certificate_redemption"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    fund_id = db.Column("fund_id", db.Integer, nullable=False)
    fund_code = db.Column("fund_code", db.String, nullable=False)
    dealing_date = db.Column("dealing_date", db.Date, nullable=False)
    redemption_quantity = db.Column("redemption_quantity", db.Numeric(10, 2), nullable=False)
    quantity = db.Column("quantity", db.Numeric(10, 2), nullable=False)
    price = db.Column("price", db.Numeric(10, 2), nullable=False)
    gross_redemption_amount = db.Column("gross_redemption_amount", db.Numeric(10, 2), nullable=False)
    total_charges = db.Column("total_charges", db.Numeric(10, 2), nullable=False)
    taxes = db.Column("taxes", db.Numeric(10, 2), nullable=False)
    net_redemption_amount = db.Column("net_redemption_amount", db.Numeric(10, 2), nullable=False)
    created_at = db.Column("created_at", db.DateTime)

    def __init__(self, fund:Fund):
        self.fund_id = fund.id
        self.fund_code = fund.name_short

def create(model:FundCertificateRedemption):
    # Prevent duplication
    existed = FundCertificateRedemption.query \
            .where( FundCertificateRedemption.fund_id == model.fund_id) \
            .where(FundCertificateRedemption.fund_code == model.fund_code) \
            .where(FundCertificateRedemption.dealing_date == model.dealing_date) \
            .where(FundCertificateRedemption.net_redemption_amount == model.net_redemption_amount) \
            .where(FundCertificateRedemption.quantity == model.quantity) \
            .first()
    if existed != None:
        return

    if model.created_at is None:
        model.created_at = datetime.now()
    db.session.add(model)
    db.session.commit()
