from flask import Blueprint, make_response, request
from flask_jwt_extended import jwt_required
from .. import util

""" Spending log """
spending_log_bp = Blueprint('spending_log', __name__, url_prefix="/spending-log")

from .spending_log import get_spending_log, update_spending_log
@spending_log_bp.route("")
@jwt_required()
def spending_log_index():
    timespan = None
    if request.args.get("timerange") is not None:
        timespan = util.Datetime.get_time_range_from_text(request.args.get("timerange"))
    elif request.args.get("from_month") is not None and request.args.get("to_month") is not None:
        from_timespan = util.Datetime.get_time_range_from_text(request.args.get("from_month"))
        to_timespan = util.Datetime.get_time_range_from_text(request.args.get("to_month"))
        timespan = (from_timespan[0], to_timespan[1],)
    if timespan is None or len(timespan) == 0:
        timespan = util.Datetime.get_time_range_from_text("today")
    return make_response({"data": get_spending_log(*timespan)})

@spending_log_bp.route("/<int:log_id>", methods=("POST",))
@jwt_required
def spending_log_detail(log_id):
    if request.method == "POST":
        update_spending_log(spending_log_id, subject=subject, amount=amount, spending_method_id=spending_method_id)

""" Spending category """
spending_category_bp = Blueprint('spending_category', __name__, url_prefix="/spending-category")

from .spending_category import get_all_spending_category, delete_spending_category, create_spending_category, update_spending_category
@spending_category_bp.route("", methods=("GET", "POST"))
@jwt_required()
def spending_category_index():
    if request.method == "GET":
        return make_response({
            "data": get_all_spending_category()
        })
    elif request.method == "POST":
        params = request.get_json()
        if params is None or "name" not in params:
            return make_response({
                "error": "Invalid data"
            }, 400)
        params.setdefault("display_name", None)
        category = create_spending_category(params["name"], display_name=params["display_name"])
        return make_response({
            "status": "ok",
            "data": category
        })

@spending_category_bp.route("/<int:category_id>", methods=("DELETE", "PUT"))
@jwt_required()
def edit_spending_category(category_id):
    if request.method == "DELETE":
        if delete_spending_category(category_id=category_id):
            return make_response({
                "status": "ok"
            })
        else:
            return make_response({
                "error": "something went wrong"
            }, 500)
    if request.method == "PUT":
        if update_spending_category(category_id, **request.get_json()):
            return make_response({
                "status": "ok"
            })
        else:
            return make_response({
                "error": "something went wrong"
            }, 500)

""" Spending method """
spending_method_bp = Blueprint('spending_method', __name__, url_prefix="/spending-method")

from ..spending.spending_method import create_spending_method, find_spending_method, get_spending_methods

@spending_method_bp.route("", methods=("GET", "POST"))
@jwt_required()
def spending_method_index():
    if request.method == "POST":
        params = request.get_json()
        spending_method = create_spending_method(
            name = params.get("name"),
            type = params.get("type"),
            alias = params.get("alias")
        )
        return make_response({"status": "ok", "data": spending_method})
    else:
        return make_response({"status": "ok", "data": get_spending_methods()})