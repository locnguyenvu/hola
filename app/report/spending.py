from datetime import datetime
from sqlalchemy.sql import text

from app.spending.category import list_all as spcategory_list_all
from app.spending.log import Log as SpendingLog
from app.di import get_db

db = get_db()


def summary_by_category(timespan: tuple) -> dict:
    categories = spcategory_list_all()
    resultset = SpendingLog.query.filter(SpendingLog.created_at.between(*timespan)).all()
    summary = {}

    total_amount = 0
    for elem in resultset:
        if elem.spending_category_id not in summary:
            category_search = list(filter(lambda cat: cat.id == elem.spending_category_id, categories))
            if len(category_search) == 0:
                continue
            category = category_search.pop()
            summary[elem.spending_category_id] = {
                "name": category.name,
                "display_name": category.display_name,
                "amount": 0,
            }

        summary[elem.spending_category_id]["amount"] += elem.amount
        total_amount += elem.amount

    return {
        "total_amount": total_amount,
        "sum_by_category": list(summary.values())
    }


def monthlytotals_bycategoryid(start_time: datetime, category_id: int):
    query = text(
        "SELECT to_char(sl.created_at, 'YYYY-MM') as pmonth, sum(sl.amount) as total "
        "FROM spending_log as sl "
        "WHERE sl.created_at > :start_time AND sl.spending_category_id = :category_id "
        "GROUP BY sl.spending_category_id, 1 "
        "ORDER BY 1 ASC"
    )
    dataset = db.session.execute(query, {
        "start_time": start_time,
        "category_id": category_id,
    }).fetchall()

    resultset = []
    for row in dataset:
        resultset.append({
            "month": row["pmonth"],
            "total": row["total"],
        })
    return resultset
