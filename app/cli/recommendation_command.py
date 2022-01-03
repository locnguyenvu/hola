import click
import re
from flask.cli import AppGroup

import app.spending.log as spending_log
import app.recommendation.spending_log_category as recommendation_spending_log_category

cli_spendinglog = AppGroup("recommendation-spending-log")
@cli_spendinglog.command("tokenize-single", with_appcontext=True)
@click.argument("spending_log_id")
def spending_log_tokenize_by_slog(spending_log_id):
    slog = spending_log.find_id(spending_log_id)
    recommendation_spending_log_category.tokenize(slog)

@cli_spendinglog.command("tokenize-all", with_appcontext=True)
def spending_log_tokenize_by_slog():
    all_slog = spending_log.Log.query.all()
    for slog in all_slog:
        if slog.spending_category_id is None:
            continue
        print("Tokenize for slog #{}".format(slog.id))
        recommendation_spending_log_category.tokenize(slog)

@cli_spendinglog.command("list-category-id", with_appcontext=True)
@click.argument("subject")
def spending_log_list_category_id(subject):
    from rich import print
    categories = recommendation_spending_log_category.list_category_id(subject)
    for cat in categories:
        print(cat.display_name)
