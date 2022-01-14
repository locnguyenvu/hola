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
    op.create_table(
            "invensment_fund",
            sa.Column("id", sa.Integer, primary_key=True, nullable=False),
            sa.Column("code", sa.String(100), unique=True, nullable=False),
            sa.Column("name", sa.String(200), unique=True, nullable=False),
            sa.Column("description", sa.String(255), unique=True, nullable=False),
            sa.Column("created_at", sa.DateTime, server_default="NOW()"),
            sa.Column("updated_at", sa.DateTime),
            )
    op.create_index(
            "idx_code",
            "invensment_fund",
            ["code"])
    pass


def downgrade():
    op.drop_index("idx_code", "invensment_fund")
    op.drop_table("invensment_fund")
    pass
