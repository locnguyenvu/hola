import click
from flask.cli import AppGroup
import app.investment.dcvfm.crawler as dcvfm_crawler

cli = AppGroup("crawler")

@cli.command("dcvfm-nav-price-history")
@click.argument("fund_name")
def dcvfm_nav_price_history(fund_name):
    crw = dcvfm_crawler.ajax()
    result = crw.get_nav_price_history(fund_name)
    from rich import print
    print(result)