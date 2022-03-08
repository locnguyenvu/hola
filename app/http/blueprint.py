from flask import Blueprint

from . import (
    auth,
    chart,
    report,
    spending_category,
    spending_log,
    spending_method,
    spending_tag,
    user,
)


auth_routes = Blueprint("auth", __name__)
auth_routes.add_url_rule("/auth/<string:session_name>", methods=["POST"], view_func=auth.login)
auth_routes.add_url_rule("/telegram-login", methods=["GET"], view_func=auth.telegram_login)
auth_routes.add_url_rule("/me", methods=["GET"], view_func=auth.me)

chart_routes = Blueprint("chart", __name__)
chart_routes.add_url_rule("/chart/expense-by-category", view_func=chart.expense_by_category)
chart_routes.add_url_rule("/chart/expense-by-month", view_func=chart.expense_by_month)

spending_log_routes = Blueprint("spending_log", __name__)
spending_log_routes.add_url_rule("/spending-log", view_func=spending_log.index)
spending_log_routes.add_url_rule("/spending-log/<int:id>", methods=["GET", "PUT"], view_func=spending_log.detail)
spending_log_routes.add_url_rule("/spending-log/<int:id>/split", methods=["POST"], view_func=spending_log.split)

spending_category_routes = Blueprint("spending_category", __name__)
spending_category_routes.add_url_rule("/spending-category", methods=["GET", "POST"], view_func=spending_category.index)
spending_category_routes.add_url_rule("/spending-category/<int:id>", methods=["DELETE", "PUT"], view_func=spending_category.edit)

spending_method_routes = Blueprint("spending_method", __name__)
spending_method_routes.add_url_rule("/spending-method", methods=["GET", "POST"], view_func=spending_method.index)

spending_tag_routes = Blueprint("spending_tag", __name__)
spending_tag_routes.add_url_rule("/spending-tag", methods=["GET", "POST"], view_func=spending_tag.index)
spending_tag_routes.add_url_rule("/spending-tag/<int:tag_id>", methods=["GET", "POST"], view_func=spending_tag.tag_log)

user_routes = Blueprint("user", __name__)
user_routes.add_url_rule("/user", view_func=user.index)

report_routes = Blueprint("report", __name__)
report_routes.add_url_rule("/report/by-month", view_func=report.summary_by_month)
report_routes.add_url_rule("/report/investment", view_func=report.investment_all)
report_routes.add_url_rule("/report/spending", view_func=report.spending_summary_by_interval)

healthcheck_routes = Blueprint("health_check", __name__)
@healthcheck_routes.route("/health-check", methods=["GET",])
def health_check():
    return {
        "status": "ok"
    }
