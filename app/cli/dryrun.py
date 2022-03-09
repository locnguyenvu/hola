from flask.cli import AppGroup
from click import argument

import app.channel
import app.bot.updates_subscriber as bot_updates_subscriber
from app.i18n import t

cli = AppGroup("dry-run")
@cli.command("broadcast-postgres-channel")
def broadcast_postgres_channel():
    app.channel.broadcast("news", dict(message="Hello, world"))

@cli.command("listen-postgres-channel")
def listen_postgres_channel():
    def handler(payload: dict):
        print(payload)

    app.channel.consume("news", handler)

@cli.command("add-subscriber")
@argument("topic")
@argument("telegram_userid")
def add_subscriber(topic, telegram_userid):
    subscriber = bot_updates_subscriber.UpdatesSubcriber()
    subscriber.topic = topic
    subscriber.telegram_userid = telegram_userid
    bot_updates_subscriber.save(subscriber)

@cli.command("delete-subscriber")
@argument("topic")
@argument("telegram_userid")
def delete_subscriber(topic, telegram_userid):
    subscriber = bot_updates_subscriber.UpdatesSubcriber.query.filter_by(topic=topic, telegram_userid=telegram_userid).first()
    if not subscriber:
        return
    bot_updates_subscriber.delete(subscriber)

@cli.command("i18n")
def i18n():
    print(t("telegram_bot.spending_log_wrong_group_error"))
