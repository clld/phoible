from clld.web.util.helpers import get_referents
from clld.db.meta import DBSession

from phoible.models import Inventory


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=['sentence', 'valueset']))


def dataset_detail_html(context=None, request=None, **kw):
    res = dict(
        (row[0], row[1]) for row in
        DBSession.execute("select source, count(pk) from inventory group by source"))
    res['inventory_count'] = DBSession.query(Inventory).count()
    return res
