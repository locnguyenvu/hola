from flask import Blueprint, make_response, request
from flask_jwt_extended import jwt_required

from .. import util
from . import spending_log, spending_category, spending_method

bp = Blueprint('spending', __name__)

""" Spending log """

@bp.route("/spending-log")
@jwt_required()
def spending_log_index():
    global spending_log
    timespan = None
    if request.args.get("timerange") is not None:
        timespan = util.Datetime.get_time_range_from_text(request.args.get("timerange"))
    elif request.args.get("from_month") is not None and request.args.get("to_month") is not None:
        from_timespan = util.Datetime.get_time_range_from_text(request.args.get("from_month"))
        to_timespan = util.Datetime.get_time_range_from_text(request.args.get("to_month"))
        timespan = (from_timespan[0], to_timespan[1],)
    if timespan is None or len(timespan) == 0:
        timespan = util.Datetime.get_time_range_from_text("today")
    
    filters = {
        "from_date": timespan[0],
        "to_date": timespan[1],
        "transaction_type": request.args.get("transaction_type")
    }

    return make_response({
        "data": list(map(lambda e: {
            "subject": e.subject,
            "amount": e.amount,
            "transaction_type": e.transaction_type,
            "payment_method": e.payment_method,
            "created_at": e.created_at
        }, spending_log.find(filters)))})

@bp.route('/spending-log/<int:log_id>', methods=('GET', 'PUT'))
@jwt_required()
def spending_log_detail(log_id):
    global spending_log
    if (request.method == 'GET') : 
        log = spending_log.find_id(log_id)
        return make_response({
            'status': 'ok',
            'data': {
                "subject": log.subject,
                "amount": log.amount,
                "transaction_type": log.transaction_type,
                "payment_method": log.payment_method,
                "created_at": log.created_at,
                "category": log.category_name,
                "category_id": log.spending_category_id
            }
        })
    if (request.method == 'PUT'):
        spending_log.edit(log_id, request.get_json())
        return make_response({'status': 'ok'})

""" Spending category """

@bp.route("/spending-category", methods=("GET", "POST"))
@jwt_required()
def spending_category_index():
    global spending_category
    if request.method == "GET":
        return make_response({
            "data": list(map(lambda e: {
                "id": e.id,
                "name": e.name,
                "display_name": e.display_name
            }, spending_category.find({})))
        })
    elif request.method == "POST":
        params = request.get_json()
        if params is None or "name" not in params:
            return make_response({
                "error": "Invalid data"
            }, 400)
        params.setdefault("display_name", None)
        category = spending_category.create(params["name"], display_name=params["display_name"])
        return make_response({
            "status": "ok",
            "data": {
                "name": category.name,
                "display_name": category.display_name
            }
        })

@bp.route("/spending-category/<int:category_id>", methods=("DELETE", "PUT"))
@jwt_required()
def edit_spending_category(category_id):
    global spending_category
    if request.method == "DELETE":
        if spending_category.delete(category_id):
            return make_response({
                "status": "ok"
            })
        else:
            return make_response({
                "error": "something went wrong"
            }, 500)
    if request.method == "PUT":
        if spending_category.edit(category_id, request.get_json()):
            return make_response({
                "status": "ok"
            })
        else:
            return make_response({
                "error": "something went wrong"
            }, 500)

""" Spending method """

@bp.route("/spending-method", methods=("GET", "POST"))
@jwt_required()
def spending_method_index():
    global spending_method
    if request.method == "POST":
        params = request.get_json()
        method = spending_method.create_spending_method(
            name = params.get("name"),
            type = params.get("type"),
            alias = params.get("alias")
        )
        return make_response({
            "status": "ok", 
            "data": {
                "id": method.id,
                "name": method.name,
                "type": method.type
            }
        })
    else:
        data = list(map(lambda e: {
            "id": e.id,
            "name": e.name,
            "type": e.type,
            "alias": e.alias
        }, spending_method.find({})))
        return make_response({"status": "ok", "data": data})

""" Spending tag """
from . import spending_tag

@bp.route("/spending-tag", methods=('GET', 'POST'))
@jwt_required()
def spending_tag_index():
    global spending_tag
    if request.method == 'GET':
        row_set = spending_tag.SpendingTag.query.all()
        data = list(map(lambda e: {
            'id': e.id, 
            'name': e.tag_name, 
            'is_active': e.is_active
        }, row_set))
        return make_response({'status': 'ok', 'data': data})
    else:
        params = request.get_json()
        spending_tag = spending_tag.create_spending_tag(
            tag_name=params.get('tag_name')
        )
        return make_response({'status': 'ok', 'tag': {'tag_name': spending_tag.tag_name, 'id': spending_tag.id}})

@bp.route("/spending-tag/<int:tag_id>", methods=('GET','POST'))
@jwt_required()
def spending_tag_tag_log(tag_id):
    if request.method == 'POST':
        params = request.get_json()
        spending_tag.edit_spending_tag(tag_id, params)
        return make_response({'status': 'ok'})
    elif request.method == 'GET':
        tagged_logs = spending_tag.get_log_with_tag(tag_id)
        total = 0
        logs = []
        for log in tagged_logs:
            total += log.amount
            logs.append({
                "spending_log_id": log.id,
                "subject": log.subject,
                "amount": log.amount
            })
        return make_response({'total': total, 'logs': logs})
