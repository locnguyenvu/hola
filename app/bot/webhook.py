from flask import Blueprint, make_response, request

from .disptacher import Distpatcher
from .command_handler import (
        login_handler,
        spending_thismonth_handler,
        spending_today_handler,
        telegram_login_handler,
    )
from .callback_query_handler import map_spending_category_callback

dispatcher = Distpatcher()

dispatcher.register_command("login", login_handler)
dispatcher.register_command("tlogin", telegram_login_handler)
dispatcher.register_command("td", spending_today_handler)
dispatcher.register_command("tm", spending_thismonth_handler)

dispatcher.register_callback("map_spending_category", map_spending_category_callback)

bp = Blueprint("telegram", __name__)
@bp.route("/telegram", methods=["POST",])
def telegram():

    payload = request.get_json(force=True)
    from rich import print
    print(payload)
    if payload == None:
        return make_response({"status": "Error"}, 400)
    dispatcher.dispatch(payload)

    return make_response({"status": "Success"}, 200)
