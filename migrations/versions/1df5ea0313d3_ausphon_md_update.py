# coding=utf-8
"""ausphon md update

Revision ID: 1df5ea0313d3
Revises: e7c4e4b2bce5
Create Date: 2019-09-30 14:18:53.654268

"""

# revision identifiers, used by Alembic.
revision = '1df5ea0313d3'
down_revision = None

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    conn = op.get_bind()
    conn.execute(
        "update contributor set description = %s, url = %s where id = 'ER'",
        (
            "An explicitly typological dataset which seeks to deal even-handedly with numerous issues that arise in the cross-linguistic comparison of Australian phoneme inventories. To understand how it was created, and how and why the inventories will appear to differ from the ultimate source documents, please read the accompanying notes (DOI: 10.5281/zenodo.3464333).",
            "https://doi.org/10.5281/zenodo.3464333",
        ))

def downgrade():
    pass

