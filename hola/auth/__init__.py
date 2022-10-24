from click import echo

from .user import User


def add_user(telegram_username, telegram_userid):
    user = User(telegram_username, telegram_userid)
    user.save()
    echo("Create success")
