from flask import Blueprint, make_response, request

from .message import Message
from .handler import LoginHandler
from .disptacher import Distpatcher

dispatcher = Distpatcher()
dispatcher.register_command("login", LoginHandler())

bp = Blueprint("telegram", __name__)
@bp.route("/telegram", methods=("GET", "POST"))
def telegram():

    payload = request.get_json(force=True)
    if payload == None:
        return make_response({"status": "Error"}, 400)
    mess = Message(payload["message"])
    dispatcher.dispatch(mess)

    return make_response({"status": "Success"}, 200)