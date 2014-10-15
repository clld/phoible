# coding=utf-8
"""issue 3

Revision ID: 6338c03c0c9
Revises: None
Create Date: 2014-10-15 11:03:54.080426

"""

# revision identifiers, used by Alembic.
revision = '6338c03c0c9'
down_revision = None

import datetime

from alembic import op
import sqlalchemy as sa


old = "http://students.washington.edu/drmccloy/pubs/McCloyEtAl2013_cunyFeatureConf.pdf"
new = "http://dan.mccloy.info/pubs/McCloyEtAl2013_cunyFeatureConf.pdf"
sql = "UPDATE source SET url = '%s' WHERE url = '%s'"

def upgrade():
    op.execute(sql % (new, old))


def downgrade():
    op.execute(sql % (old, new))
