import re

from sqlalchemy.orm import joinedload
from markdown import markdown

from clld.web.util.helpers import get_referents
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, Language, Source, Contributor
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML

from phoible.models import Inventory


def readme(text):
    lines = []
    for line in text.split('\n'):
        if line.strip().startswith('# '):
            continue
        if line.strip().startswith('#'):
            line = '##' + line
        lines.append(line)
    return markdown('\n'.join(lines))


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=['sentence', 'valueset']))


def desc(req, d, sources=None):
    if sources is None:
        sources = {k: Source.get(k) for k in
                   'MoisikEsling2011 Hayes2009 Moran2012a Moran_etal2012'.split()}
    if not d:
        return d
    for k, v in sources.items():
        a = link(req, v)
        d = re.sub(r'\*\*(?P<id>%s)\*\*' % k, str(a), d)
    return d


def dataset_detail_html(context=None, request=None, **kw):
    res = {}#dict(
        #(row[0], row[1]) for row in
        #DBSession.execute("select source, count(pk) from inventory group by source"))
    res['inventory_count'] = DBSession.query(Inventory).count()
    res['segment_count'] = DBSession.query(Parameter).count()
    res['language_count'] = DBSession.query(Language).count()
    res['contributors'] = DBSession.query(Contributor).order_by(Contributor.name).options(
        joinedload(Contributor.contribution_assocs),
        joinedload(Contributor.references)).all()
    res['sources'] = {
        k: Source.get(k) for k in
        ['MoisikEsling2011', 'IPA2005', 'Hayes2009', 'Moran2012a', 'Moran_etal2012',
         'Cysouw_etal2012', 'mccloy_etal2013']}
    res['descriptions'] = {c.id: desc(request, c.description, res['sources'])
                           for c in res['contributors']}
    return res


def segment_link(req, glyph, segments, ns=False):
    if glyph not in segments:
        if ns:
            return ''
        return HTML.a(
            glyph, name="glyph-" + glyph, style='font-size: 1em; color: lightgray;')
    res = link(req, segments[glyph])
    del segments[glyph]
    return res
