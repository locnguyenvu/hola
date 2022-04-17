import app.recommendation.spending_log_category as recommendation_spending_log_category
import app.spending.log as spending_log
import app.spending.category as spending_category
from app.botnext.telegram import CallbackQuery
from app.botnext.callbackquery.base import CallbackQueryHandler


class MapSpendingCategory(CallbackQueryHandler):

    def _process(self, query: CallbackQuery):
        args = query.function_arguments()

        sl = spending_log.find_id(args["log_id"])
        sc = spending_category.find_id(args["category_id"])
        sl.spending_category_id = sc.id
        spending_log.save(sl)
        query.edit_message_text(f"{sl.subject} -> {sc.display_name}")

        recommendation_spending_log_category.tokenize(sl)
        pass
