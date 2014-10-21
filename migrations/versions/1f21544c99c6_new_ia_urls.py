# coding=utf-8
"""new IA urls

Revision ID: 1f21544c99c6
Revises: 359f0ac0bfcc
Create Date: 2014-10-21 20:27:10.339133

"""

# revision identifiers, used by Alembic.
revision = '1f21544c99c6'
down_revision = '359f0ac0bfcc'

import datetime

from alembic import op
import sqlalchemy as sa
from path import path

from clld.db.migration import Connection
from clld.lib.dsv import reader
from clld.db.models.common import Contribution

import phoible
from phoible.models import Inventory


def upgrade():
    csv = path(phoible.__file__).dirname().joinpath(
        '..', 'data', 'InventoryID-InternetArchive.csv')
    ia_urls = {row[0]: row[1] for row in reader(csv) if row[1] != 'NA'}

    conn = Connection(op.get_bind())
    for id_, url in ia_urls.items():
        pk = conn.pk(Contribution, id_)
        conn.update(Inventory, dict(internetarchive_url=url), pk=pk)


def downgrade():
    pass
