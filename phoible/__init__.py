from clld.web.app import get_configurator

from phoible import models
from phoible import maps
from phoible import datatables


_ = lambda s: s
_('Contribution')
_('Contributions')
_('Parameter')
_('Parameters')
_('Alternative names')
_('Unit Parameter')
_('Unit Parameters')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'contributions': '/inventories',
        'contribution': '/inventories/view/{id:[^/\.]+}',
    }
    settings['sitemaps'] = ['language', 'source', 'parameter', 'contribution', 'valueset']
    config = get_configurator('phoible', settings=settings)
    config.include('clldmpg')
    config.register_map('contribution', maps.InventoryMap)
    config.add_static_view('data', 'phoible:static/data')
    config.include('phoible.datatables')
    config.include('phoible.adapters')
    return config.make_wsgi_app()
