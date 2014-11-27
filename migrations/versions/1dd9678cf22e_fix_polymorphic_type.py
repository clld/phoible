# coding=utf-8
"""fix polymorphic_type

Revision ID: 1dd9678cf22e
Revises: 1f21544c99c6
Create Date: 2014-11-26 15:24:14.763000

"""

# revision identifiers, used by Alembic.
revision = '1dd9678cf22e'
down_revision = '1f21544c99c6'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    update_pmtype(['language', 'parameter', 'contribution'], 'base', 'custom')


def downgrade():
    update_pmtype(['language', 'parameter', 'contribution'], 'custom', 'base')


def update_pmtype(tablenames, before, after):
    for table in tablenames:
        op.execute(sa.text('UPDATE %s SET polymorphic_type = :after '
            'WHERE polymorphic_type = :before' % table
            ).bindparams(before=before, after=after))
