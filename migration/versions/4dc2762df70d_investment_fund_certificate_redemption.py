"""investment_fund_certificate_redemption

Revision ID: 4dc2762df70d
Revises: a6bcf315d5bb
Create Date: 2022-02-03 20:04:24.702156+07:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '4dc2762df70d'
down_revision = 'a6bcf315d5bb'
branch_labels = None
depends_on = None

config_table = table('config', 
    column('path', sa.String),
    column('value', sa.String)
)

def upgrade():

    op.bulk_insert(config_table, [
        {"path": "investment.dcvfm.redemption_email", "value": ""}
    ])

    op.create_table(
        "investment_fund_certificate_redemption",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("fund_id", sa.Integer, nullable=False),
        sa.Column("fund_code", sa.String, nullable=False),
        sa.Column("dealing_date", sa.Date, nullable=False),
        sa.Column("redemption_quantity", sa.Numeric(10, 2), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 2), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("gross_redemption_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("total_charges", sa.Numeric(10, 2), nullable=False),
        sa.Column("taxes", sa.Numeric(10, 2), nullable=False),
        sa.Column("net_redemption_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default="NOW()")
    )
    op.create_index( "idx_ifcr_dealing_date", "investment_fund_certificate_redemption", ["dealing_date"])
    pass


def downgrade():
    op.execute(
        config_table.delete().where(config_table.c.path=="investment.dcvfm.redemption_email")
    )
    op.drop_index("idx_ifcr_dealing_date", "investment_fund_certificate_redemption")
    op.drop_table("investment_fund_certificate_redemption")
    pass
