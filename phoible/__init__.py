from sqlalchemy.orm import joinedload
from pyramid.config import Configurator

from clld.web.app import MapMarker, CtxFactoryQuery
from clld import interfaces
from clld.web.adapters.download import Download
from clld.db.models.common import Contributor, ContributionContributor
from clldutils.svg import icon, data_url
from clld.web.app import menu_item

import functools
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
                joinedload(Contributor.contribution_assocs).joinedload(ContributionContributor.contribution)
            )
        return query


class PhoibleMapMarker(MapMarker):
    def __call__(self, ctx, req):
        color = '#000000'
        if interfaces.ILanguage.providedBy(ctx):
            color = ctx.jsondata['color']
        elif interfaces.IValueSet.providedBy(ctx):
            color = ctx.language.jsondata['color']
        elif isinstance(ctx, tuple):
            try:
                color = ctx[0].jsondata['color']
            except KeyError:
                raise ValueError(ctx)

        return data_url(icon('c' + color[1:]))


class RdfDump(Download):
    ext = 'n3'


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'contributions': '/inventories',
        'contribution': r'/inventories/view/{id:[^/\.]+}',
    }
    config = Configurator(settings=settings)

    config.include('clldmpg')
    config.registry.registerUtility(PhoibleMapMarker(), interfaces.IMapMarker)
    config.registry.registerUtility(PhoibleCtxFactoryQuery(), interfaces.ICtxFactoryQuery)
    config.add_static_view('data', 'phoible:static/data')
    # config.register_download(RdfDump(Dataset, 'phoible', description='RDF dump'))

    config.add_route('faq', '/faq')
    config.add_route('conventions', '/conventions')
    home_comp = config.registry.settings['home_comp']
    home_comp.append('faq')
    home_comp.append('conventions')

    config.register_menu(
        ('dataset', functools.partial(menu_item, 'dataset', label='Home')),
        ('contributors', functools.partial(menu_item, 'contributors', label='Contributors')),
        ('contributions', functools.partial(menu_item, 'contributions', label='Inventories')),
        ('languages', functools.partial(menu_item, 'languages', label='Languages')),
        ('parameters', functools.partial(menu_item, 'parameters', label='Segments')),
        ('sources', functools.partial(menu_item, 'sources', label='Sources')),
        ('conventions', functools.partial(menu_item, 'conventions', label='Conventions')),
        ('faq', functools.partial(menu_item, 'faq', label='FAQ')),
    )

    return config.make_wsgi_app()
