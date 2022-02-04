"""dcvfm_crawler

Revision ID: aa4221bc4049
Revises: 4ebc0c876f23
Create Date: 2022-01-18 20:01:00.151947+07:00

"""
from alembic import op
from sqlalchemy.sql import table, column
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa4221bc4049'
down_revision = '4ebc0c876f23'
branch_labels = None
depends_on = None

config_table = table('config', 
    column('path', sa.String),
    column('value', sa.String)
)

def upgrade():
    op.bulk_insert(config_table, [
        {"path": "investment.dcvfm.crawler.base_url_ajax", "value": ""}
    ])
    pass


def downgrade():
    op.execute(
        config_table.delete().where(config_table.c.path=="investment.dcvfm.crawler.base_url_ajax")
    )
    pass
