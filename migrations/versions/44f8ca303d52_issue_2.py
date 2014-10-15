# coding=utf-8
"""issue 2

Revision ID: 44f8ca303d52
Revises: 6338c03c0c9
Create Date: 2014-10-15 11:15:18.217174

"""

# revision identifiers, used by Alembic.
revision = '44f8ca303d52'
down_revision = '6338c03c0c9'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""\
UPDATE source SET
bibtex_type = 'incollection',
address = 'Canberra',
booktitle = 'Tibeto-Burman Languages of Nepal: Manange and Sherpa',
editor = 'Carol Genetti',
title = 'A Grammar and Dictionary of the Manange Language',
publisher = 'Pacific Linguistics',
pages = '2-189',
startpage_int = 2,
pages_int = 187,
note = NULL
WHERE id = 'nmmhildebrandt2004'""")


def downgrade():
    pass

