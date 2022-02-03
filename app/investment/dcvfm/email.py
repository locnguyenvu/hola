import bs4
from datetime import datetime
from flask import current_app
from email.message import Message
from rich import print

import app.investment.fund as investment_fund
from app.investment import fund_certificate_subscription as fcs, fund_certificate_redemption as fcr
from app.util import strings 

SUBSCRIPTION_EMAIL = current_app.config.get("investment.dcvfm.subscription_email")
REDEMPTION_EMAIL = current_app.config.get("investment.dcvfm.redemption_email")

class InvalidEmailException(Exception):
    pass

class DcvfmSubscriptionConfirmation:

    def __init__(self, email_message: Message):
        self.email_message = email_message
        pass

    def get_content(self) -> str:
        content = ""
        for part in self.email_message.walk():
            if part.get_content_type() != "text/html":
                continue 
            content = part.get_payload(decode=True)
        return content

    def process(self):
        if not self.email_message.is_multipart():
            raise InvalidEmailException("Email format must be multipart")

        dcvfm_funds = investment_fund.list_dcfvm()
        html_content = self.get_content()
        soup = bs4.BeautifulSoup(html_content, 'html.parser')

        # Search for fund name
        paragraphs = soup.find_all("p")

        fund_name = paragraphs[2].text
        target_fund = None
        for fund in dcvfm_funds:
            if fund_name.strip() == fund.name_long.strip():
                target_fund = fund
    
        if target_fund is None:
            raise InvalidEmailException("Fund not found")

        tables = soup.find_all("table")
        subscription_table = tables[3]

        if len(subscription_table.tbody.tr.find_all(["th", "tr"])) != 8:
            raise InvalidEmailException("Subscription info not found")

        transcation_row = subscription_table.tbody.find_all(["tr"])[2]
        transaction_columns = transcation_row.find_all(["tr", "th"])

        dealing_date = transaction_columns[0].text
        gross_subscription_amount = transaction_columns[2].text
        actual_subscription_amount = transaction_columns[3].text
        total_charge = transaction_columns[4].text
        net_subscription_amount = transaction_columns[5].text
        subscription_price = transaction_columns[6].text
        quantity_unit = transaction_columns[7].text

        subscription = fcs.FundCertificateSubscription(target_fund)
        subscription.dealing_date = datetime.strptime(dealing_date, "%d/%m/%Y")
        subscription.gross_subscription_amount = strings.todecimal(gross_subscription_amount),
        subscription.actual_subscription_amount = strings.todecimal(actual_subscription_amount),
        subscription.total_charges = strings.todecimal(total_charge),
        subscription.net_subscription_amount = strings.todecimal(net_subscription_amount),
        subscription.subscription_price = strings.todecimal(subscription_price),
        subscription.quantity = strings.todecimal(quantity_unit)

        fcs.create(subscription)
        pass


class DcvfmRedemptionConfirmation:

    def __init__(self, email_message: Message):
        self.email_message = email_message
        pass

    def get_content(self) -> str:
        content = ""
        for part in self.email_message.walk():
            if part.get_content_type() != "text/html":
                continue 
            content = part.get_payload(decode=True)
        return content

    def process(self):
        if not self.email_message.is_multipart():
            raise InvalidEmailException("Email format must be multipart")

        dcvfm_funds = investment_fund.list_dcfvm()
        html_content = self.get_content()
        soup = bs4.BeautifulSoup(html_content, 'html.parser')

        # Search for fund name
        paragraphs = soup.find_all("p")

        fund_name = paragraphs[2].text
        target_fund = None
        for fund in dcvfm_funds:
            if fund_name.strip() == fund.name_long.strip():
                target_fund = fund
    
        if target_fund is None:
            raise InvalidEmailException("Fund not found")

        tables = soup.find_all("table")
        redemption_table = tables[3]

        if len(redemption_table.tbody.tr.find_all(["th", "tr"])) != 9:
            raise InvalidEmailException("Subscription info not found")

        transcation_row = redemption_table.tbody.find_all(["tr"])[2]
        transaction_columns = transcation_row.find_all(["tr", "th"])

        dealing_date = transaction_columns[0].text
        redemption_quantity = transaction_columns[2].text
        quantity_unit = transaction_columns[3].text
        redemption_price = transaction_columns[4].text
        gross_redemption_amount = transaction_columns[5].text
        total_charges = transaction_columns[6].text
        taxes = transaction_columns[7].text
        net_redemption_amount = transaction_columns[8].text

        redemption = fcr.FundCertificateRedemption(target_fund)
        redemption.dealing_date = datetime.strptime(dealing_date, "%d/%m/%Y")
        redemption.gross_redemption_amount = strings.todecimal(gross_redemption_amount),
        redemption.total_charges = strings.todecimal(total_charges),
        redemption.net_redemption_amount = strings.todecimal(net_redemption_amount),
        redemption.price = strings.todecimal(redemption_price),
        redemption.quantity = strings.todecimal(quantity_unit)
        redemption.taxes = strings.todecimal(taxes)
        redemption.redemption_quantity = strings.todecimal(redemption_quantity)

        fcr.create(redemption)
        pass
