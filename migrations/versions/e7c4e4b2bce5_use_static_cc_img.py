# coding=utf-8
"""use static cc img

Revision ID: e7c4e4b2bce5
Revises: c345fdbdf07a
Create Date: 2018-08-14 09:37:54.884899

"""

# revision identifiers, used by Alembic.
revision = 'e7c4e4b2bce5'
down_revision = 'c345fdbdf07a'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""UPDATE dataset SET jsondata = '{"license_name": "Creative Commons Attribution-ShareAlike 3.0 Unported License", "license_icon": "cc-by-sa.png"}' WHERE jsondata = '{"license_name": "Creative Commons Attribution-ShareAlike 3.0 Unported License", "license_icon": "http://i.creativecommons.org/l/by-sa/3.0/88x31.png"}' """)

def downgrade():
    pass

