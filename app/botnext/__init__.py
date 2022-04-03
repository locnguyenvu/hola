from flask import current_app
from .dispatcher import Dispatcher
from .callbackquery.map_spending_category import MapSpendingCategory
from .command.help import HelpCommand
from .command.income_input import IncomeInputCommand
from .command.spending_thismonth import SpendingThisMonthCommand
from .groupchat.spending_log import SpendingLogGroupChat

webhook_dispatcher = Dispatcher()
webhook_dispatcher.register_command("help", HelpCommand())
webhook_dispatcher.register_command("tm", SpendingThisMonthCommand())
webhook_dispatcher.register_command("ii", IncomeInputCommand())

webhook_dispatcher.register_groupchat(current_app.config.get("telegram.group.spending_log"), SpendingLogGroupChat())

webhook_dispatcher.register_callback("map_spending_category", MapSpendingCategory())
