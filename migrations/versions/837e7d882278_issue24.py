# coding=utf-8
"""issue24

Revision ID: 837e7d882278
Revises: 1df5ea0313d3
Create Date: 2021-01-20 12:27:44.016804

"""

# revision identifiers, used by Alembic.
revision = '837e7d882278'
down_revision = '1df5ea0313d3'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("update source set name = trim(trailing '}' from name)")

def downgrade():
    pass

