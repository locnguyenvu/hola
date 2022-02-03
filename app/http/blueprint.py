from flask import Blueprint

from . import (
    auth_controller,
    chart_controller,
    investment_controller,
    spending_category_controller,
    spending_log_controller,
    spending_method_controller,
    spending_tag_controller,
    user_controller,
)


auth = Blueprint("auth", __name__)
auth.add_url_rule("/auth/<string:session_name>", methods=["POST"], view_func=auth_controller.login)
auth.add_url_rule("/telegram-login", methods=["GET"], view_func=auth_controller.telegram_login)
auth.add_url_rule("/me", methods=["GET"], view_func=auth_controller.me)

chart = Blueprint("chart", __name__)
chart.add_url_rule("/chart/expense-by-category", view_func=chart_controller.expense_by_category)
chart.add_url_rule("/chart/expense-by-month", view_func=chart_controller.expense_by_month)

spending_log = Blueprint("spending_log", __name__)
spending_log.add_url_rule("/spending-log", view_func=spending_log_controller.index)
spending_log.add_url_rule("/spending-log/<int:id>", methods=["GET", "PUT"], view_func=spending_log_controller.detail)
spending_log.add_url_rule("/spending-log/<int:id>/split", methods=["POST"], view_func=spending_log_controller.split)

spending_category = Blueprint("spending_category", __name__)
spending_category.add_url_rule("/spending-category", methods=["GET", "POST"], view_func=spending_category_controller.index)
spending_category.add_url_rule("/spending-category/<int:id>", methods=["DELETE", "PUT"], view_func=spending_category_controller.edit)

spending_method = Blueprint("spending_method", __name__)
spending_method.add_url_rule("/spending-method", methods=["GET", "POST"], view_func=spending_method_controller.index)

spending_tag = Blueprint("spending_tag", __name__)
spending_tag.add_url_rule("/spending-tag", methods=["GET", "POST"], view_func=spending_tag_controller.index)
spending_tag.add_url_rule("/spending-tag/<int:tag_id>", methods=["GET", "POST"], view_func=spending_tag_controller.tag_log)

user = Blueprint("user", __name__)
user.add_url_rule("/user", view_func=user_controller.index)

investment = Blueprint("investment", __name__)
investment.add_url_rule("/investment", view_func=investment_controller.index)
