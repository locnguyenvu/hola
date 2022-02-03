"""nav_price_change_history

Revision ID: a6bcf315d5bb
Revises: aa4221bc4049
Create Date: 2022-01-26 20:48:21.005178+07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6bcf315d5bb'
down_revision = 'aa4221bc4049'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "investment_fund_nav_price_history",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("fund_id", sa.Integer, nullable=False),
        sa.Column("fund_code", sa.String, nullable=False),
        sa.Column("update_date", sa.Date, nullable=False),
        sa.Column("dealing_date", sa.Date, nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("net_change", sa.Numeric(10, 2), nullable=False),
        sa.Column("probation_change", sa.Numeric(10, 2), nullable=False),
        sa.Column("is_active", sa.Integer, default=0),
        sa.Column("created_at", sa.DateTime, server_default="NOW()")
    )
    op.create_index( "idx_ifnph_dealing_date", "investment_fund_nav_price_history", ["dealing_date"])
    pass


def downgrade():
    op.drop_index("idx_ifnph_dealing_date", "investment_fund_nav_price_history")
    op.drop_table("investment_fund_nav_price_history")
    pass
