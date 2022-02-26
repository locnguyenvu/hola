import asyncio
import click, time
from flask.cli import AppGroup
from datetime import datetime

import app.investment.dcvfm.crawler as dcvfm_crawler
from app.di import get_bot
from app.investment import fund, fund_nav_price_history
import app.bot.updates_subscriber as bot_updates_subscriber

bot = get_bot()
cli = AppGroup("crawler")

@cli.command("dcvfm-nav-history")
@click.option("-f", "--fund-name")
def dcvfm_nav_price_history(fund_name):
    s = time.perf_counter()
    crw = dcvfm_crawler.ajax()

    if fund_name != None:
        funds = fund.Fund.query.filter_by(name_short=fund_name.upper(), group=fund.DCVFM).all()
    else:
        funds = fund.list_dcfvm()
    for fu in funds:
        resultset = crw.fetch_nav_price_history(fu.name_short.lower())
        for row in resultset:
            p_change = fund_nav_price_history.FundNavPriceHistory(fu)
            p_change.dealing_date = row["dealing_date"]
            p_change.update_date = row["update_date"]
            p_change.price = row["nav_price"]
            p_change.net_change = row["net_change"]
            p_change.probation_change = row["probation_change"]
            if fund_nav_price_history.existed(p_change):
                break
            fund_nav_price_history.save(p_change)
    elapsed = time.perf_counter() - s
    print(f"Execute in {elapsed:0.2f} second")

@cli.command("dcvfm-nav-latest")
def dcvfm_nav():
    s = time.perf_counter()
    _ = asyncio.run(fund_nav_price_history.crawl_latest_all_dcvfm_nav())
    elapsed = time.perf_counter() - s
    print(f"Execute in {elapsed:0.2f} second")
    dcvfm_funds = fund.list_dcfvm(update_today=False)
    dcvfm_updates = fund_nav_price_history.find_active_by_fund_ids(list(map(lambda e: e.id, dcvfm_funds)))
    if len(dcvfm_funds) == 0 or len(dcvfm_funds) != len(dcvfm_updates):
        return

    changes = list(map(lambda e: str(e), dcvfm_updates))
    cur_date = datetime.now()
    message = ["DCVFM nav price {}".format(cur_date.strftime("%Y-%m-%d")), "{:-<26}".format("-")] + changes 

    subscribers = bot_updates_subscriber.get_subscribers("investment.dcvfm-nav-price-change")
    for subscriber in subscribers:
        bot.send_message(chat_id=subscriber.telegram_userid, text="\n".join(message))
