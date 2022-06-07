from app import util
from app.income.log import Log as IncomeLog
from app.investment.fund_certificate_subscription import FundCertificateSubscription
from app.spending.log import Log as SpendingLog

def by_month(month:str):
    timerange = util.dt.timerange_fromtext(month)

    total_income = 0
    incomes = IncomeLog.query.filter(IncomeLog.created_at.between(*timerange)).all() 
    for inc in incomes:
        total_income += inc.amount

    total_investment = 0
    investments = FundCertificateSubscription.query.filter(FundCertificateSubscription.dealing_date.between(*timerange)).all()
    for invt in investments:
        total_investment += invt.net_subscription_amount

    total_spending = 0
    spendings = SpendingLog.query.filter(SpendingLog.created_at.between(*timerange)).all()
    for spd in spendings:
        total_spending += spd.amount

    return {
        "income": util.numeric.floatval(total_income),
        "investment": util.numeric.floatval(total_investment),
        "spending": util.numeric.floatval(total_spending),
    }
