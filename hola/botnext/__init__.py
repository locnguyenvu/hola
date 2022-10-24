from .dispatcher import Dispatcher
from .callbackquery.map_spending_category import MapSpendingCategory
from .callbackquery.spending_category import AddSpendingCategory, EditSpendingCategory
from .callbackquery.setup import SetupSpendingLogGroupChat
from .command.income_input import IncomeInputCommand
from .command.investment_overview import InvestmentOverviewCommand
from .command.login import LoginCommand
from .command.setup import SetupCommand
from .command.spending_thismonth import SpendingThisMonthCommand
from .command.spending_category import SpendingCategoryCommand

webhook_dispatcher = Dispatcher()

webhook_dispatcher.register_command("ii", IncomeInputCommand())
webhook_dispatcher.register_command("io", InvestmentOverviewCommand())
webhook_dispatcher.register_command("login", LoginCommand())
webhook_dispatcher.register_command("setup", SetupCommand())
webhook_dispatcher.register_command("spendingcategory", SpendingCategoryCommand())
webhook_dispatcher.register_command("tm", SpendingThisMonthCommand())

webhook_dispatcher.register_callback("map_spending_category", MapSpendingCategory())
webhook_dispatcher.register_callback("setup_spending_log_chatgroup", SetupSpendingLogGroupChat())
webhook_dispatcher.register_callback("spending_category_add", AddSpendingCategory())
webhook_dispatcher.register_callback("spending_category_edit", EditSpendingCategory())
