from flask import Blueprint, make_response, request, current_app, abort
from telegram import Message 
from app.di import get_bot
from rich import print
from .disptacher import Distpatcher
from .command import (
    help,
    income_input,
    init_spending_log_group,
    investment_report,
    login,
    reconcile_account,
    spending_thismonth,
    spending_today,
    telegram_login,
)
from .callbackquery import (
    map_spending_category
)

bot = get_bot()
dispatcher = Distpatcher()

dispatcher.register_command("help", help.handle)
dispatcher.register_command("ii", income_input.handle)
dispatcher.register_command("init_slg", init_spending_log_group.handle)
dispatcher.register_command("ivr", investment_report.handle)
dispatcher.register_command("login", login.handle)
dispatcher.register_command("ra", reconcile_account.handle)
dispatcher.register_command("td", spending_today.handle)
dispatcher.register_command("tlogin", telegram_login.handle)
dispatcher.register_command("tm", spending_thismonth.handle)

dispatcher.register_callback("map_spending_category", map_spending_category.handle)



bp = Blueprint("telegram", __name__)
@bp.route("/telegram", methods=["POST",])
def telegram():
    secret = request.args.get("x-bot")
    if secret is None or secret != current_app.config.get("TELEGRAM_WEBHOOK_SECRET"):
        return abort(401)

    payload = request.get_json(force=True)
    print(payload)
    mess = Message.de_json(payload["message"], bot)
    print(mess)


    if payload == None:
        return make_response({"status": "Error"}, 400)
    dispatcher.dispatch(payload)

    return make_response({"status": "Success"}, 200)
