"""add_fund_update_weekday

Revision ID: fefd711708a3
Revises: 5329e9eddefa
Create Date: 2022-02-26 20:03:13.410846+07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fefd711708a3'
down_revision = '5329e9eddefa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("investment_fund", sa.Column("update_weekday", sa.String(7), default="0000000"))

    fund_table = sa.sql.table("investment_fund",\
        sa.Column("name_short", sa.String),
        sa.Column("update_weekday", sa.String(7))
    )

    op.execute(fund_table.update()\
            .where(fund_table.c.name_short == op.inline_literal('DCDS'))\
            .values({"update_weekday": op.inline_literal("1111100")})
    )
    op.execute(fund_table.update()\
            .where(fund_table.c.name_short == op.inline_literal('DCBC'))\
            .values({"update_weekday": op.inline_literal("1111100")})
    )
    op.execute(fund_table.update()\
            .where(fund_table.c.name_short == op.inline_literal('DCIP'))\
            .values({"update_weekday": op.inline_literal("1111100")})
    )
    op.execute(fund_table.update()\
            .where(fund_table.c.name_short == op.inline_literal('DCBF'))\
            .values({"update_weekday": op.inline_literal("0000100")})
    )
    
    pass


def downgrade():
    op.drop_column("investment_fund", "update_weekday")
    pass
