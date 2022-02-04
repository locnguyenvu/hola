from .fund import Fund
from .fund_certificate_subscription import FundCertificateSubscription
from .fund_certificate_redemption import FundCertificateRedemption

def overview() -> dict:
    subscriptions = FundCertificateSubscription.query.all()
    redemptions = FundCertificateRedemption.query.all()
    fund_ids = list(set(map(lambda sub: sub.fund_id, subscriptions)))
    funds = Fund.query.filter(Fund.id.in_(fund_ids)).all()

    fund_dict = {}
    for f in funds:
        if f.id in fund_dict:
            continue
        fund_dict[f.id] = {
            "name": f.name_long,
            "code": f.name_short,
            "quantity": 0,
            "nav_price": f.nav_price,
            "total_value": 0,
        }

    net_value = 0
    current_value = 0

    for sub in subscriptions:
        fund_dict[sub.fund_id]["quantity"] += sub.quantity
        net_value += sub.net_subscription_amount

    for red in redemptions:
        fund_dict[red.fund_id]["quantity"] -= red.quantity
        net_value -= red.net_redemption_amount 

    for fid in fund_dict:
        fund_dict[fid]["total_value"] = round(fund_dict[fid]["quantity"] * fund_dict[fid]["nav_price"], 2)
        current_value += fund_dict[fid]["total_value"]


    return {
        "net_value": net_value,
        "current_value": current_value,
        "interest_rate": "{:.2f}%".format((current_value - net_value)/ net_value * 100),
        "detail": fund_dict,
    }
