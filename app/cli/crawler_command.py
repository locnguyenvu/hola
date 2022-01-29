import click
from flask.cli import AppGroup

import app.investment.dcvfm.crawler as dcvfm_crawler
from app.investment import fund, fund_nav_price_history


cli = AppGroup("crawler")

@cli.command("dcvfm-nav-price-history")
@click.argument("fund_name")
def dcvfm_nav_price_history(fund_name):
    crw = dcvfm_crawler.ajax()
    result = crw.get_nav_price_history(fund_name)
    fund_m = fund.find_dcvfm_by_code(fund_name.upper())
    for row in result:
        pricechange_m = fund_nav_price_history.FundNavPriceHistory(fund_m)
        pricechange_m.dealing_date = row["dealing_date"]
        pricechange_m.update_date = row["update_date"]
        pricechange_m.price = row["nav_price"]
        pricechange_m.net_change = row["net_change"]
        pricechange_m.probation_change = row["probation_change"]
        fund_nav_price_history.create(pricechange_m)

    #print(fnd)
    #print(result)