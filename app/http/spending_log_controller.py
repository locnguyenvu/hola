from flask import make_response, request
from flask_jwt_extended import jwt_required

import app.spending.log as spending_log
from app import util

@jwt_required()
def index():
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
        "transaction_type": request.args.get("transaction_type"),
        "spending_category_id": request.args.get("category_id")
    }

    return make_response({
        "data": list(map(lambda e: {
            "id": e.id,
            "subject": e.subject,
            "amount": e.amount,
            "transaction_type": e.transaction_type,
            "payment_method": e.payment_method,
            "created_at": e.created_at
        }, spending_log.find(filters)))})

@jwt_required()
def detail(id):
    if (request.method == 'GET') : 
        log = spending_log.find_id(id)
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
        spending_log.edit(id, request.get_json())
        return make_response({'status': 'ok'})