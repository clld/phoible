from clld.web.app import get_configurator
from clld.interfaces import IParameter, IUnit, ILinkAttrs

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


def link_attrs(req, obj, **kw):
    #if IUnit.providedBy(obj):
    #    id_ = obj.glyph.id if obj.glyph else obj.id
    #    kw['href'] = req.route_url('parameter', id=id_, **kw.pop('url_kw', {}))
    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'contributions': '/inventories',
        'contribution': '/inventories/view/{id:[^/\.]+}',
    }
    settings['sitemaps'] = ['language', 'source', 'parameter', 'contribution', 'valueset']
    config = get_configurator('phoible', (link_attrs, ILinkAttrs), settings=settings)
    config.register_map('contribution', maps.InventoryMap)
    config.add_static_view('data', 'phoible:static/data')
    config.include('phoible.datatables')
    config.include('phoible.adapters')
    return config.make_wsgi_app()
