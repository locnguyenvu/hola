"""bot_broadcast_news

Revision ID: 5329e9eddefa
Revises: 3c9a9fa808e8
Create Date: 2022-02-10 17:26:57.414379+07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5329e9eddefa'
down_revision = '3c9a9fa808e8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "bot_updates_subscriber",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("topic", sa.String, nullable=False),
        sa.Column("telegram_userid", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime),
    )
    pass


def downgrade():
    op.drop_table("bot_updates_subscriber")
    pass
