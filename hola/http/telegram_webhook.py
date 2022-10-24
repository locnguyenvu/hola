from flask import abort, current_app, request, make_response
from app.botnext import webhook_dispatcher


def handle():
    secret = request.args.get("x-bot")
    if secret is None or secret != current_app.config.get("TELEGRAM_WEBHOOK_SECRET"):
        return abort(401)
    payload = request.get_json(force=True)

    if payload is None:
        return make_response({"status": "Error"}, 400)
    webhook_dispatcher.dispatch(payload)
    return make_response({"status": "ok"})
    pass
