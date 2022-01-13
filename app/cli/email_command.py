import re
import click
import imaplib
import email
import os
from rich import print, inspect
from email.header import decode_header
from flask import current_app
from flask.cli import AppGroup, with_appcontext
from bs4 import BeautifulSoup, element

cli = AppGroup('email')

@cli.command("read", with_appcontext=True)
def read():

    server = imaplib.IMAP4_SSL(current_app.config.get("EMAIL_HOST"))
    server.login(current_app.config.get("EMAIL_ACCOUNT"), current_app.config.get("EMAIL_PASSWORD"))

    server.select("INBOX")
    status, data = server.search(None, 'ALL')
    if status != "OK":
        click.echo("Failed to search unseen mail")
        return

    for num in data[0].split():
        _, imap_content = server.fetch(num, '(RFC822)')

        if len(imap_content) == 1 and imap_content[0] == None:
            continue

        for raw_email in imap_content:
            if not isinstance(raw_email, tuple):
                continue

            # parse a bytes email into a message object
            email_message = email.message_from_bytes(raw_email[1])
            # decode the email subject
            subject, encoding = decode_header(email_message["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            mail_from, encoding = decode_header(email_message.get("From"))[0]
            if isinstance(mail_from, bytes):
                mail_from = mail_from.decode(encoding)

            mail_to, encoding = decode_header(email_message.get("To"))[0]
            if isinstance(mail_to, bytes):
                mail_to = mail_to.decode(encoding)

            print("From: " + mail_from)
            print("To: " + mail_to)
            print("Subject: " + subject)

            if email_message.is_multipart():
                for part in email_message.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    #content_disposition = str(part.get("Content-Disposition"))
                    try:
                        body = part.get_payload(decode=True).decode()
                        #if content_type == "text/plain":
                        #    plain_text_file.write(body.encode("utf-8"))
                        if content_type == "text/html":
                            parse_email_content(body.encode("utf-8"))
                    except:
                        pass

    return

def parse_email_content(email_content):
    soup = BeautifulSoup(email_content, 'html.parser')

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
        click.echo("Subscription info not found")


    transcation_row = subscription_table.tbody.find_all(["tr"])[2]
    transaction_columns = transcation_row.find_all(["tr", "th"])

    dealing_date = transaction_columns[0].text
    gross_subscription_amount = transaction_columns[2].text
    actual_subscription_amount = transaction_columns[3].text
    total_charge = transaction_columns[4].text
    net_subsription_amount = transaction_columns[5].text
    subscription_price = transaction_columns[6].text
    quantity_unit = transaction_columns[7].text

    print("Fund name: " + fund_name)
    print("Dealing date: " + dealing_date)
    print("Gross subscription amount: " + gross_subscription_amount)
    print("Actual subscription amount: " + actual_subscription_amount)
    print("Total charge: " + total_charge) 
    print("Net subsription amount: " + net_subsription_amount) 
    print("Subscription price: " + subscription_price) 
    print("Quantity unit: " + quantity_unit)