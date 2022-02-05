"""package_income

Revision ID: 3bc0628e48b1
Revises: 4dc2762df70d
Create Date: 2022-02-04 09:43:14.270851+07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bc0628e48b1'
down_revision = '4dc2762df70d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "income_log",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("subject", sa.String, nullable=False),
        sa.Column("amount", sa.Numeric(10,2), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default="NOW()"),
        sa.Column("updated_at", sa.DateTime),
    )
    pass


def downgrade():
    op.drop_table("income_log")
    pass
