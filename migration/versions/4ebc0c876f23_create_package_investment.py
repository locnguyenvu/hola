"""create_package_investment

Revision ID: 4ebc0c876f23
Revises: 
Create Date: 2022-01-13 16:37:49.736627+07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ebc0c876f23'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    
    tbl_investment_fund = op.create_table(
        "investment_fund",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("code", sa.String(100), unique=True, nullable=False),
        sa.Column("name_short", sa.String(200), unique=True, nullable=False),
        sa.Column("name_long", sa.String(255), unique=True, nullable=False),
        sa.Column("nav_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("group", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default="NOW()"),
        sa.Column("updated_at", sa.DateTime),
    )
    op.create_index( "idx_if_code", "investment_fund", ["code"])
    op.bulk_insert(tbl_investment_fund, [
        {"code": "VFMVF1", "name_short": "DCDS", "name_long": "QUỸ ĐẦU TƯ CHỨNG KHOÁN VIỆT NAM (VFMVF1) | VIETNAM SECURITIES INVESTMENT FUND", "nav_price": 0.00, "group": "dcvfm"},
        {"code": "VFMVF4", "name_short": "DCBC", "name_long": "QUỸ ĐẦU TƯ DOANH NGHIỆP HÀNG ĐẦU VIỆT NAM (VFMVF4) | VIETNAM BLUE-CHIP FUND", "nav_price": 0.00, "group": "dcvfm"},
        {"code": "VFMVFB", "name_short": "DCBF", "name_long": "QUỸ ĐẦU TƯ TRÁI PHIẾU VIỆT NAM (VFMVFB) | VIETNAM BOND FUND", "nav_price": 0.00, "group": "dcvfm"},
        {"code": "DCIP", "name_short": "DCIP", "name_long": "QUỸ ĐẦU TƯ ĐỊNH HƯỚNG BẢO TOÀN VỐN VIỆT NAM | VIETNAM CAPITAL PROTECTION ORIENTED FUND", "nav_price": 0.00, "group": "dcvfm"},
    ])

    op.create_table(
        "investment_fund_certificate_subscription",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("fund_id", sa.Integer, nullable=False),
        sa.Column("fund_code", sa.String, nullable=False),
        sa.Column("dealing_date", sa.Date, nullable=False),
        sa.Column("gross_subscription_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("actual_subscription_amount", sa.Numeric(10,2), nullable=False),
        sa.Column("total_charges", sa.Numeric(10, 2), nullable=False),
        sa.Column("net_subscription_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("subscription_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default="NOW()")
    )
    op.create_index( "idx_ifcs_created_at", "investment_fund_certificate_subscription", ["created_at"])
    pass


def downgrade():
    op.drop_index("idx_if_code", "investment_fund")
    op.drop_table("investment_fund")
    op.drop_index( "idx_ifcs_created_at", "investment_fund_certificate_subscription")
    op.drop_table("investment_fund_certificate_subscription")
    pass
