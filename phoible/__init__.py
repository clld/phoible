from sqlalchemy.orm import joinedload_all

from clld.web.app import get_configurator, MapMarker, CtxFactoryQuery
from clld import interfaces, RESOURCES
from clld.web.adapters.download import Sqlite
from clld.db.models.common import Dataset, Contributor, ContributionContributor

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


class PhoibleMapMarker(MapMarker):
    def get_icon(self, ctx, req):
        if interfaces.ILanguage.providedBy(ctx) and ctx.genus:
            return ctx.genus.ficon

        if isinstance(ctx, (list, tuple)) and ctx[0].genus:
            return ctx[0].genus.ficon


class RdfDump(Sqlite):
    ext = 'n3'


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'contributions': '/inventories',
        'contribution': '/inventories/view/{id:[^/\.]+}',
    }
    settings['sitemaps'] = ['language', 'source', 'parameter', 'contribution', 'valueset']
    config = get_configurator(
        'phoible',
        (PhoibleMapMarker(), interfaces.IMapMarker),
        (PhoibleCtxFactoryQuery(), interfaces.ICtxFactoryQuery),
        settings=settings)

    config.include('clldmpg')
    config.include('phoible.maps')
    config.add_static_view('data', 'phoible:static/data')
    config.include('phoible.datatables')
    config.include('phoible.adapters')

    #rsc_map = {
    #    'language': 'Languages',
    #    'parameter': 'Segments',
    #    'contribution': 'Inventories',
    #    'valueset': 'PhonemeMatrix',
    #}
    config.register_download(RdfDump(Dataset, 'phoible', description='RDF dump'))
    #for rsc in RESOURCES:
    #    if rsc.name in rsc_map:
    #        config.register_download(N3Dump(
    #            rsc.model, 'phoible', description="%s as RDF" % rsc_map[rsc.name]))

    return config.make_wsgi_app()
