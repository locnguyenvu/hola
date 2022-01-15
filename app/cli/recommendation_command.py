import click
from flask.cli import AppGroup

import app.spending.log as spending_log
import app.recommendation.spending_log_category as recommendation_spending_log_category

cli_spendinglog = AppGroup("recommendation-spending-log")
@cli_spendinglog.command("tokenize-single", with_appcontext=True)
@click.argument("spending_log_id")
def spending_log_tokenize_by_single_log(spending_log_id):
    slog = spending_log.find_id(spending_log_id)
    recommendation_spending_log_category.tokenize(slog)

@cli_spendinglog.command("tokenize-all", with_appcontext=True)
@click.option("-s", "--from-time", "from_time", type=str, required=False)
def spending_log_tokenize_by_bulk_log(from_time):
    query = spending_log.Log.query
    if from_time is not None:
        query = query.filter(spending_log.Log.created_at > from_time)

    all_slog = query.filter().all()
    for slog in all_slog:
        if slog.spending_category_id is None:
            continue
        print("Tokenize for slog #{}".format(slog.id))
        recommendation_spending_log_category.tokenize(slog)

@cli_spendinglog.command("list-category-id", with_appcontext=True)
@click.argument("subject")
def spending_log_list_category_id(subject):
    categories = recommendation_spending_log_category.list_categories(subject)
    for cat in categories:
        print(f"{cat.id:>3}. {cat.display_name}")


@cli_spendinglog.command("remove-context", with_appcontext=True)
@click.argument("subject")
def spending_log_remove_context(subject):
    categories = recommendation_spending_log_category.list_categories(subject)
    for cat in categories:
        print(f"{cat.id:>3}. {cat.display_name}")

    del_catid = input("Deleted category id>>>")
    if not del_catid.isnumeric():
        click.echo("Invalid option, should be numeric")
        return
    recommendation_spending_log_category.remove_context(subject, int(del_catid))

