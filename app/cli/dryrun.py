from flask.cli import AppGroup

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
    from rich import print
    timerange = util.dt.timerange_prevmonth(6)

    groupbymonth = {}
    limitcate = spending_category.list_limited()
    for cat in limitcate:
        result = report_spending.monthlytotals_bycategoryid(timerange[0], cat.id)
        for elem in result:
            if elem["month"] not in groupbymonth.keys():
                groupbymonth[elem["month"]] = {}
            groupbymonth[elem["month"]][cat.id] = elem["total"]

    for cat in limitcate:
        for key in groupbymonth.keys():
            if cat.id not in groupbymonth[key].keys():
                groupbymonth[key][cat.id] = 0
    print(groupbymonth)
