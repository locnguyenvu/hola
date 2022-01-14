import bs4
import re
from datetime import datetime
from flask import current_app

from app.util import parse_str_decimal

SUBSCRIPTION_EMAIL = current_app.config.get("investment.dcvfm.subscription_email")

class InvalidEmail(Exception):
    pass

class SubscriptionConfirmationResult(object):

    def __init__(self, 
            fund_name: str, 
            dealing_date: datetime, 
            gross_subscription_amount: float,
            actual_subscription_amount: float,
            total_charges: float,
            net_subscription_amount: float,
            subscription_price: float,
            quantity: float):
        self.fund_name = fund_name
        self.dealing_date = dealing_date
        self.gross_subscription_amount = gross_subscription_amount
        self.actual_subscription_amount = actual_subscription_amount
        self.total_charges = total_charges
        self.net_subscription_amount = net_subscription_amount
        self.subscription_price = subscription_price
        self.quantity = quantity
        pass

def parse_email_content(email_content):
    soup = bs4.BeautifulSoup(email_content, 'html.parser')

    # Search for fund name
    paragraphs = soup.find_all("p")
    fund_name = ""
    for pa in paragraphs:
        for pa_child in pa.children:
            match = re.search(r"(VFMVFB|VFMVF1|VFMVF4)", pa_child.text)
            if match is not None:
                fund_name = match[0]
                break

    subscription_table = None
    tables = soup.find_all("table")
    for table in tables:
        tbody = table.tbody
        table_header = tbody.tr

        numer_of_columns = len(table_header.find_all(["th", "td"]))
        if numer_of_columns == 8:
            subscription_table = table
            break

    if subscription_table is None or not fund_name:
        raise InvalidEmail("Subcription info or Fund name is not found")


    transcation_row = subscription_table.tbody.find_all(["tr"])[2]
    transaction_columns = transcation_row.find_all(["tr", "th"])

    dealing_date = transaction_columns[0].text
    gross_subscription_amount = transaction_columns[2].text
    actual_subscription_amount = transaction_columns[3].text
    total_charge = transaction_columns[4].text
    net_subscription_amount = transaction_columns[5].text
    subscription_price = transaction_columns[6].text
    quantity_unit = transaction_columns[7].text

    subscription_result = SubscriptionConfirmationResult(
        fund_name = fund_name,
        dealing_date = datetime.strptime(dealing_date, "%d/%m/%Y"),
        gross_subscription_amount = parse_str_decimal(gross_subscription_amount),
        actual_subscription_amount = parse_str_decimal(actual_subscription_amount),
        total_charges = parse_str_decimal(total_charge),
        net_subscription_amount = parse_str_decimal(net_subscription_amount),
        subscription_price = parse_str_decimal(subscription_price),
        quantity = parse_str_decimal(quantity_unit)
    )
    return subscription_result

