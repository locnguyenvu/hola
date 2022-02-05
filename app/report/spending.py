from app.spending.category import list_all as spcategory_list_all
from app.spending.log import Log as SpendingLog

def summary_by_category(timespan:tuple) -> dict:
    categories = spcategory_list_all()
    resultset = SpendingLog.query.filter(SpendingLog.created_at.between(*timespan)).all()
    summary = {}

    total_amount = 0
    for elem in resultset:
        if elem.spending_category_id not in summary:
            category_search = list(filter(lambda cat: cat.id == elem.spending_category_id, categories))
            if len(category_search) == False:
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