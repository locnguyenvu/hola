from .dispatcher import Dispatcher
from .callbackquery.map_spending_category import MapSpendingCategory
from .command.help import HelpCommand
from .command.income_input import IncomeInputCommand
from .command.investment_overview import InvestmentOverviewCommand
from .command.login import LoginCommand
from .command.setup_spending_log_groupchat import SetupSpendingLogGroupChatCommand
from .command.spending_thismonth import SpendingThisMonthCommand

webhook_dispatcher = Dispatcher()

webhook_dispatcher.register_command("help", HelpCommand())
webhook_dispatcher.register_command("ii", IncomeInputCommand())
webhook_dispatcher.register_command("io", InvestmentOverviewCommand())
webhook_dispatcher.register_command("login", LoginCommand())
webhook_dispatcher.register_command("setup_spending_log_groupchat", SetupSpendingLogGroupChatCommand())
webhook_dispatcher.register_command("tm", SpendingThisMonthCommand())

webhook_dispatcher.register_callback("map_spending_category", MapSpendingCategory())
