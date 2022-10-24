from . import auth
from . import chart
from . import report
from . import spending_category
from . import spending_log
from . import spending_tag
from . import telegram_webhook as _tw
from . import user
from flask import Blueprint


def health_check():
    return {
        "status": "ok"
    }


telegram_webhook = Blueprint("telegram_webhook", __name__)
telegram_webhook.add_url_rule("/telegram-next", methods=["POST", ], view_func=_tw.handle)

web_api = Blueprint("web_api", __name__)
web_api.add_url_rule("/auth/<string:session_name>", methods=["POST"], view_func=auth.login)
web_api.add_url_rule("/telegram-login", methods=["GET"], view_func=auth.telegram_login)
web_api.add_url_rule("/me", methods=["GET"], view_func=auth.me)
web_api.add_url_rule("/chart/expense-by-category", view_func=chart.expense_by_category)
web_api.add_url_rule("/chart/expense-by-month", view_func=chart.expense_by_month)
web_api.add_url_rule("/chart/watch-monthly-expense", view_func=chart.watch_monthlyexpense)
web_api.add_url_rule("/health", view_func=health_check)
web_api.add_url_rule("/report/by-month", view_func=report.summary_by_month)
web_api.add_url_rule("/report/investment", view_func=report.investment_all)
web_api.add_url_rule("/report/spending", view_func=report.spending_summary_by_interval)
web_api.add_url_rule("/spending-category", methods=["GET", "POST"], endpoint="spending_category_index", view_func=spending_category.index)
web_api.add_url_rule("/spending-category/<int:id>", methods=["DELETE", "PUT"], endpoint="spending_category_edit", view_func=spending_category.edit)
web_api.add_url_rule("/spending-log", endpoint="spending_log_index", view_func=spending_log.index)
web_api.add_url_rule("/spending-log/<int:id>", methods=["GET", "PUT"], endpoint="spending_log_detail", view_func=spending_log.detail)
web_api.add_url_rule("/spending-log/<int:id>/split", methods=["POST"], endpoint="spending_log_split", view_func=spending_log.split)
web_api.add_url_rule("/spending-tag", methods=["GET", "POST"], endpoint="spending_tag_index", view_func=spending_tag.index)
web_api.add_url_rule("/spending-tag/<int:tag_id>", methods=["GET", "POST"], endpoint="spending_tag_tag_log", view_func=spending_tag.tag_log)
web_api.add_url_rule("/user", endpoint="user_index", view_func=user.index)


def init_app(app):
    app.register_blueprint(web_api)
    app.register_blueprint(telegram_webhook)
