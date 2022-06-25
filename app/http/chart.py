from flask import request, make_response
from flask_jwt_extended import jwt_required
from dateutil.relativedelta import relativedelta
from datetime import datetime

from app.util import dt
import app.report.spending as report_spending
import app.spending.log as spending_log
import app.spending.category as spending_category


@jwt_required()
def expense_by_category():
    if request.args.get('timerange') is not None:
        timespan = dt.timerange_fromtext(request.args.get('timerange'))
    elif request.args.get("from_month") is not None and request.args.get("to_month") is not None:
        from_timespan = dt.timerange_fromtext(request.args.get("from_month"))
        to_timespan = dt.timerange_fromtext(request.args.get("to_month"))
        timespan = (from_timespan[0], to_timespan[1],)
    else:
        timespan = dt.timerange_fromtext('current_month')

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
        months = dt.timerange_fromtext(request.args.get('timerange'))
    if request.args.get('starting_month') is not None:
        starting_month = request.args.get('starting_month')

    timespan = dt.timerange_prevmonth(months, starting_month=starting_month)

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


@jwt_required()
def watch_monthlyexpense():
    monthrange = 6
    timerange = dt.timerange_prevmonth(monthrange)

    milestone = timerange[0]
    nowc = datetime.now().strftime("%Y-%m")
    timerangekeys = [milestone.strftime("%Y-%m")]
    while milestone.strftime("%Y-%m") != nowc:
        milestone = milestone + relativedelta(months=1)
        timerangekeys.append(milestone.strftime("%Y-%m"))

    groupbytimeindex = {}
    limitcate = spending_category.list_limited()
    for cat in limitcate:
        result = report_spending.monthlytotals_bycategoryid(timerange[0], cat.id)
        for timeindex in timerangekeys:
            if timeindex not in groupbytimeindex:
                groupbytimeindex[timeindex] = []
            if timeindex in result.keys():
                groupbytimeindex[timeindex].append(result[timeindex])
                continue
            groupbytimeindex[timeindex].append(0)

    filleddata = []
    for i, v in enumerate(limitcate):
        element = {
            "name": v.display_name,
            "data": []
        }
        for fil in groupbytimeindex.values():
            element["data"].append(fil[i])

        filleddata.append(element)
    return make_response({
        "key": timerangekeys,
        "data": filleddata,
    })
