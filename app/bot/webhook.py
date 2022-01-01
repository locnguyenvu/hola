from flask import Blueprint, make_response, request
from app.telebot import get_bot

from .message import Message
from .disptacher import get_dispatcher

bot = get_bot()
disptacher = get_dispatcher()

bp = Blueprint("telegram", __name__)
@bp.route("/telegram", methods=("GET", "POST"))
def telegram():

    payload = request.get_json(force=True)
    if payload == None:
        return make_response({"status": "Error"}, 400)
    mess = Message(payload["message"])
    disptacher.dispatch(mess)

    return make_response({"status": "Success"}, 200)

