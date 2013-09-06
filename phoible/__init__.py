from clld.web.app import get_configurator
from clld.interfaces import IParameter, IUnit, ILinkAttrs

from phoible.adapters import GeoJsonFeature
from phoible import models


def link_attrs(req, obj, **kw):
    if IUnit.providedBy(obj):
        # we are about to link to a language details page: redirect to contribution page!
        print obj
        id_ = obj.glyph.id if obj.glyph else obj.id
        kw['href'] = req.route_url('parameter', id=id_, **kw.pop('url_kw', {}))
    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = get_configurator('phoible', (link_attrs, ILinkAttrs), settings=settings)
    config.register_adapter(GeoJsonFeature, IParameter)
    return config.make_wsgi_app()
