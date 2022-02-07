"""chat_bot_context

Revision ID: 3c9a9fa808e8
Revises: 3bc0628e48b1
Create Date: 2022-02-05 14:53:22.216981+07:00

"""
from xmlrpc.client import DateTime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c9a9fa808e8'
down_revision = '3bc0628e48b1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "bot_chat_context",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("context", sa.String, nullable=False),
        sa.Column("telegram_userid", sa.String, nullable=False),
        sa.Column("telegram_username", sa.String, nullable=False),
        sa.Column("chat_id", sa.String, nullable=False),
        sa.Column("handler_builder", sa.JSON, nullable=False),
        sa.Column("is_active", sa.SmallInteger, nullable=False, default="0"),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    pass


def downgrade():
    op.drop_table("bot_chat_context")
    pass
