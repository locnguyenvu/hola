from flask import Blueprint, request, make_response
from flask_jwt_extended import jwt_required

from ..util import Datetime
from ..spending import spending_log, spending_category

bp = Blueprint('chart', __name__)

@bp.route("/chart")
@jwt_required()
def current_month():
    if request.args.get('timerange') is not None:
        timespan = Datetime.get_time_range_from_text(request.args.get('timerange'))
    else:
        timespan = Datetime.get_time_range_from_text('current_month')
    
    report_logs = spending_log.find({
        "from_date": timespan[0],
        "to_date": timespan[1]
    })

    total_spending_amount = 0
    group_by_category = {}
    for slog in report_logs:
        total_spending_amount += int(slog.amount)
        if slog.spending_category_id not in group_by_category:
            category = spending_category.find_id(slog.spending_category_id)
            group_by_category[slog.spending_category_id] = {
                "id": category.id,
                "name": category.name,
                "dis_name": category.display_name,
                "value": 0
            }
        group_by_category[slog.spending_category_id]['value'] += int(slog.amount)

    value_only = list(map(lambda e: e['value'], group_by_category.values()))
    value_only.sort(reverse=True)

    categories = []
    for amount in value_only:
        result = list(filter(lambda cat, amnt=amount: cat['value'] == amnt, group_by_category.values()))
        categories.append(list(result).pop())


    return make_response({
        "total": total_spending_amount,
        "categories": categories,
        "from_date": timespan[0],
        "to_date": timespan[1]
    })

@bp.route("/chart/previous-months")
@jwt_required()
def previous_months():
    return make_response({"status": "ok"})