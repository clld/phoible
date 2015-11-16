# coding=utf-8
"""fix wikipedia URLs

Revision ID: 505cc11480ce
Revises: 1dd9678cf22e
Create Date: 2015-11-16 16:10:35.992444

"""

# revision identifiers, used by Alembic.
revision = '505cc11480ce'
down_revision = '1dd9678cf22e'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""UPDATE parameter SET jsondata = '{}' WHERE jsondata = '{"wikipedia_url": "http://en.wikipedia.org//www.mediawiki.org/"}'""")


def downgrade():
    pass
