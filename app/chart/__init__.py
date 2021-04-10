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

    return make_response({
        "total": total_spending_amount,
        "group_by_categories": list(group_by_category.values())
    })

@bp.route("/chart/previous-months")
@jwt_required()
def previous_months():
    return make_response({"status": "ok"})