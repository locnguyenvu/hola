from flask.cli import AppGroup
from dateutil.relativedelta import relativedelta
from datetime import datetime

import app.util as util
import app.channel
import app.report.spending as report_spending
import app.spending.category as spending_category
from app.i18n import t

cli = AppGroup("dry-run")


@cli.command("broadcast-postgres-channel")
def broadcast_postgres_channel():
    app.channel.broadcast("news", dict(message="Hello, world"))


@cli.command("listen-postgres-channel")
def listen_postgres_channel():
    def handler(payload: dict):
        print(payload)

    app.channel.consume("news", handler)


@cli.command("i18n")
def i18n():
    print(t("telegram_bot.spending_log_wrong_group_error"))


@cli.command("report")
def report():
    monthrange = 6
    from rich import print
    timerange = util.dt.timerange_prevmonth(monthrange)

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
    print({
        "key": timerangekeys,
        "data": filleddata,
    })
