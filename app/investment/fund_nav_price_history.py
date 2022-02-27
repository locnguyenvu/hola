import aiohttp, asyncio
from datetime import datetime
from app.di import get_db

from .fund import Fund, list_dcfvm
from .dcvfm import crawler as dcvfm_crawler

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

def save(model:FundNavPriceHistory):
    if not model.created_at:
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

def mark_active(navPrice:FundNavPriceHistory):
    FundNavPriceHistory.query.filter_by(fund_id=navPrice.fund_id, is_active=1).update({"is_active": 0})
    Fund.query.filter_by(id=navPrice.fund_id).update({"nav_price": navPrice.price})
    navPrice.is_active = 1
    save(navPrice)

def find_active_by_fund_ids(fund_ids: list) -> list:
    query = FundNavPriceHistory.query.filter_by(is_active=1).filter(FundNavPriceHistory.fund_id.in_(fund_ids))
    return query.all()

async def crawl_latest_dcvfm_nav_by_fund(crawler: dcvfm_crawler.ajax, fund:Fund) -> FundNavPriceHistory:
    resultset = await crawler.afetch_nav_price_history(fund.name_short)

    latest_result = resultset[0]
    latest_change = FundNavPriceHistory(fund)
    latest_change.dealing_date = latest_result["dealing_date"]
    latest_change.update_date = latest_result["update_date"]
    latest_change.price = latest_result["nav_price"]
    latest_change.net_change = latest_result["net_change"]
    latest_change.probation_change = latest_result["probation_change"]

    if not existed(latest_change):
        mark_active(latest_change)
        return latest_change
    return None


async def crawl_latest_all_dcvfm_nav():
    funds = list_dcfvm(update_today=True)

    async with aiohttp.ClientSession() as session:
        crawler = dcvfm_crawler.ajax(session=session)
        tasks = []
        for fund in funds:
            if not fund.has_updated_today():
                tasks.append(crawl_latest_dcvfm_nav_by_fund(crawler, fund))

        result = await asyncio.gather(*tasks)
        return result