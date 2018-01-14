import re

from sqlalchemy.orm import joinedload_all
from pyramid.httpexceptions import HTTPMovedPermanently, HTTPNotFound
from pyramid.config import Configurator

from clld.web.app import MapMarker, CtxFactoryQuery
from clld import interfaces
from clld.web.adapters.download import Download
from clld.db.models.common import (
    Dataset, Contributor, ContributionContributor, Parameter, Config,
)

from phoible import models
assert models

_ = lambda s: s
_('Contribution')
_('Contributions')
_('Parameter')
_('Parameters')
_('Alternative names')
_('Unit Parameter')
_('Unit Parameters')


class PhoibleCtxFactoryQuery(CtxFactoryQuery):
    def refined_query(self, query, model, req):
        if model == Contributor:
            query = query.options(
                joinedload_all(
                    Contributor.contribution_assocs,
                    ContributionContributor.contribution,
                )
            )
        return query

    def __call__(self, model, req):
        if model == Parameter:
            # responses for no longer supported legacy codes
            if re.match('[0-9]{1,4}$', req.matchdict['id']):
                rec = req.db.query(Config)\
                    .filter(Config.key == '__glyphid_%s__' % req.matchdict['id']).first()
                if rec:
                    raise HTTPMovedPermanently(
                        location=req.route_url('parameter', id=rec.value))
                else:
                    raise HTTPNotFound()
        return super(PhoibleCtxFactoryQuery, self).__call__(model, req)


class PhoibleMapMarker(MapMarker):
    def get_icon(self, ctx, req):
        if interfaces.ILanguage.providedBy(ctx) and ctx.genus:
            return ctx.genus.ficon

        if isinstance(ctx, (list, tuple)) and ctx[0].genus:
            return ctx[0].genus.ficon


class RdfDump(Download):
    ext = 'n3'


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'contributions': '/inventories',
        'contribution': '/inventories/view/{id:[^/\.]+}',
    }
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(PhoibleMapMarker(), interfaces.IMapMarker)
    config.registry.registerUtility(PhoibleCtxFactoryQuery(), interfaces.ICtxFactoryQuery)
    config.add_static_view('data', 'phoible:static/data')
    config.register_download(RdfDump(Dataset, 'phoible', description='RDF dump'))
    return config.make_wsgi_app()
