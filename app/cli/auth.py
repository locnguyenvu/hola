import click
import re
from flask import current_app
from flask.cli import AppGroup

from werkzeug.security import generate_password_hash
from app.user import find_by_telegram_account
from app.auth import login_session

cli = AppGroup("auth")
@cli.command('register', with_appcontext=True)
@click.argument('username')
def cli_register_user(username):
    user = find_by_telegram_account(username)
    if user is None:
        print(f'\n!Err: {username} does not exit\n')
        return
    pin = ''
    while re.match(r'^\d{4}$', pin.strip()) is None:
        pin = input('Pin (4 digits): ')

    user.pin = generate_password_hash(pin)
    user.save()
    print(f'\nSuccess!\n')
    

@cli.command("new-login-session", with_appcontext=True)
@click.argument('username')
def cli_new_session(username):
    user = find_by_telegram_account(username)
    if user is None:
        print(f'\n!Err: {username} does not exit\n')
        return
    session = login_session.new_login_session(user.id)
    print(session)
    login_url = "{web_base_url}/login/{session_name}?otp={otp}".format(
            web_base_url = current_app.config["WEB_BASE_URL"],
            session_name = session.session_name,
            otp = session.otp)

    click.echo(f"Login url: {login_url}")