from collections import OrderedDict
from functools import partial

from clld.web.app import get_configurator, MapMarker, menu_item
from clld import interfaces, RESOURCES
from clld.web.adapters.download import N3Dump

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


class PhoibleMapMarker(MapMarker):
    def get_icon(self, ctx, req):
        if interfaces.ILanguage.providedBy(ctx) and ctx.genus:
            return ctx.genus.ficon

        if isinstance(ctx, (list, tuple)) and ctx[0].genus:
            return ctx[0].genus.ficon


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'contributions': '/inventories',
        'contribution': '/inventories/view/{id:[^/\.]+}',
    }
    settings['sitemaps'] = ['language', 'source', 'parameter', 'contribution', 'valueset']
    #settings['navbar.inverse'] = True
    config = get_configurator(
        'phoible', (PhoibleMapMarker(), interfaces.IMapMarker), settings=settings)


    menuitems = OrderedDict()
    for plural in 'contributions languages parameters sources'.split():
        menuitems[plural] = partial(menu_item, plural)
    config.registry.registerUtility(menuitems, interfaces.IMenuItems)



    config.include('clldmpg')
    config.include('phoible.maps')
    config.add_static_view('data', 'phoible:static/data')
    config.include('phoible.datatables')
    config.include('phoible.adapters')

    rsc_map = {
        'language': 'Languages',
        'parameter': 'Segments',
        'contribution': 'Inventories',
        'valueset': 'PhonemeMatrix',
    }

    for rsc in RESOURCES:
        if rsc.name in rsc_map:
            config.register_download(N3Dump(
                rsc.model, 'phoible', description="%s as RDF" % rsc_map[rsc.name]))

    return config.make_wsgi_app()
