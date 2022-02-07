from flask import request, make_response
from flask_jwt_extended import jwt_required

from app.util import dt 
import app.spending.log as spending_log
import app.spending.category as spending_category


@jwt_required()
def expense_by_category():
    if request.args.get('timerange') is not None:
        timespan = dt.time_range_from_text(request.args.get('timerange'))
    elif request.args.get("from_month") is not None and request.args.get("to_month") is not None:
        from_timespan = dt.time_range_from_text(request.args.get("from_month"))
        to_timespan = dt.time_range_from_text(request.args.get("to_month"))
        timespan = (from_timespan[0], to_timespan[1],)
    else:
        timespan = dt.time_range_from_text('current_month')
    
    report_logs = spending_log.find({
        "from_date": timespan[0],
        "to_date": timespan[1]
    })

    total_spending_amount = 0
    group_by_category = {}
    for slog in report_logs:
        if slog.spending_category_id is None:
            continue
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
        "from_month": timespan[0].strftime('%Y-%m'),
        "to_month": timespan[1].strftime('%Y-%m')
    })

@jwt_required()
def expense_by_month():
    months = 6
    starting_month = None 
    if request.args.get('months') is not None:
        months = dt.time_range_from_text(request.args.get('timerange'))
    if request.args.get('starting_month') is not None:
        starting_month = request.args.get('starting_month')

    timespan = dt.time_range_in_past_month(months, starting_month=starting_month)
    
    report_logs = spending_log.find({
        "from_date": timespan[0],
        "to_date": timespan[1]
    })
    report = {}
    total = 0
    for slog in report_logs:
        key = slog.created_at.strftime('%Y-%m')
        if key not in report:
            report[key] = {"key": key, "value": 0}
        report[key]["value"] += slog.amount
        total += slog.amount

    return make_response({
        "months": list(report.values()), 
        "total": total,
        "from_month": timespan[0].strftime('%Y-%m'),
        "to_month": timespan[1].strftime('%Y-%m')
    })
