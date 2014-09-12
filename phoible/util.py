from __future__ import unicode_literals
import re

from sqlalchemy.orm import joinedload
from six import text_type

from clld.web.util.helpers import get_referents
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, Language, Source, Contributor
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML

from phoible.models import Inventory


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=['sentence', 'valueset']))


def desc(req, d, sources=None):
    if sources is None:
        sources = {k: Source.get(k) for k in 'moisikesling2011 hayes2009 moran2012a moranetal2012'.split()}
    if not d:
        return d
    for k, v in sources.items():
        a = link(req, v)
        d = re.sub('\*\*(?P<id>%s)\*\*' % k, text_type(a), d)
    return d


def dataset_detail_html(context=None, request=None, **kw):
    res = dict(
        (row[0], row[1]) for row in
        DBSession.execute("select source, count(pk) from inventory group by source"))
    res['inventory_count'] = DBSession.query(Inventory).count()
    res['segment_count'] = DBSession.query(Parameter).count()
    res['language_count'] = DBSession.query(Language).count()
    #res['moran'] = Source.get('moran2012a')
    #res['moisik'] = Source.get('moisikesling2011')
    #res['hayes'] = Source.get('hayes2009')
    res['contributors'] = DBSession.query(Contributor).order_by(Contributor.name).options(
            joinedload(Contributor.contribution_assocs),
            joinedload(Contributor.references)).all()
    res['sources'] = {k: Source.get(k) for k in 'moisikesling2011 ipa2005 hayes2009 moran2012a moranetal2012 cysouwetal2012 mccloyetal2013'.split()}
    res['descriptions'] = {c.id: desc(request, c.description, res['sources'])
                           for c in res['contributors']}
    return res


def segment_link(req, glyph, segments, ns=False):
    #if glyph not in segments:
    #    for modifier in ['\u0303', '\u02d0']:
    #        if not glyph.endswith(modifier):
    #            if glyph + modifier in segments:
    #                glyph += modifier
    #                break

    if glyph not in segments:
        if ns:
            return ''
        return HTML.a(
            glyph, name="glyph-" + glyph, style='font-size: 1em; color: lightgray;')
    res = link(req, segments[glyph])
    del segments[glyph]
    return res
