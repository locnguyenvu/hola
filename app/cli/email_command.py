import email
import imaplib
import click
import traceback
from email.header import decode_header
from flask import current_app
from flask.cli import AppGroup
from rich import print, inspect
import app.investment.dcvfm.email as dcvfm_email

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

            try:
                # parse a bytes email into a message object
                email_message = email.message_from_bytes(raw_email[1])
                # decode the email subject
                subject, encoding = decode_header(email_message["Subject"])[0]
                if encoding is None:
                    encoding = "utf-8"
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                mail_from, _ = decode_header(email_message.get("From"))[0]
                if isinstance(mail_from, bytes):
                    mail_from = mail_from.decode(encoding)

                mail_to, _ = decode_header(email_message.get("To"))[0]
                if isinstance(mail_to, bytes):
                    mail_to = mail_to.decode(encoding)

                print("From: " + mail_from)
                print("To: " + mail_to)
                print("Subject: " + subject)

                if email_message.is_multipart():
                    for part in email_message.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/html":
                            body = part.get_payload(decode=True)
                            if mail_to == dcvfm_email.SUBSCRIPTION_EMAIL:
                                subscription_result = dcvfm_email.parse_email_content(body)
                                inspect(subscription_result)

            except dcvfm_email.InvalidEmail as e:
                print(type(e))
            except Exception as e:
                print(type(e))
                print(traceback.print_exc())

    return

