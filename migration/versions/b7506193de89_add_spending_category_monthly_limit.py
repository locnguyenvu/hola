"""add-spending-category-monthly-limit

Revision ID: b7506193de89
Revises: fefd711708a3
Create Date: 2022-06-07 07:59:44.298108+07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7506193de89'
down_revision = 'fefd711708a3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("spending_category", sa.Column("monthly_limit", sa.FLOAT, default=0))
    pass


def downgrade():
    op.drop_column("spending_category", "monthly_limit")
    pass
