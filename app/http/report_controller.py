from datetime import datetime

from flask import request, make_response
from flask_jwt_extended import jwt_required

import app.report.overview
import app.report.investment
import app.report.spending
from app.util import dt
from .helper import response_error, response_success

@jwt_required()
def summary_by_month():
    period_str = request.args.get("timespan")
    if not period_str or len(period_str) == 0:
        period_str = dt.CURRENT_MONTH

    return make_response({
        "data": app.report.overview.by_month(period_str)
    })


@jwt_required()
def investment_all():
    return make_response({
        "data": app.report.investment.all()
    })

@jwt_required()
def spending_summary_by_interval():
    if not request.args.get('from') or not request.args.get("to"):
        return response_error(400, "missing required arguments")

    try:
        time_from = datetime.fromisoformat(request.args.get("from"))
        time_to = datetime.fromisoformat(request.args.get("to"))
        return response_success(app.report.spending.summary_by_category((time_from, time_to)))
    except Exception as e:
        return response_error(400, str(e))
