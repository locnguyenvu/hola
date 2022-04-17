from .blueprint import *
from . import telegram_webhook as _tw
from flask import Blueprint

telegram_webhook = Blueprint("telegram_webhook", __name__)
telegram_webhook.add_url_rule("/telegram-next", methods=["POST", ], view_func=_tw.handle)


def init_app(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(chart_routes)
    app.register_blueprint(healthcheck_routes)
    app.register_blueprint(report_routes)
    app.register_blueprint(spending_category_routes)
    app.register_blueprint(spending_log_routes)
    app.register_blueprint(spending_method_routes)
    app.register_blueprint(spending_tag_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(telegram_webhook)
