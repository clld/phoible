from sqlalchemy.orm import joinedload
from pyramid.config import Configurator

from clld.web.app import MapMarker, CtxFactoryQuery
from clld import interfaces
from clld.web.adapters.download import Download
from clld.db.models.common import Contributor, ContributionContributor
from clldutils.svg import icon, data_url

import clld
import os
import filecmp
from shutil import copyfile


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


def sync_clld_mako():
    """ This function syncs project/templates/app.mako project/templates/util.mako with ones in the clld library.
    """
    clld_app_mako_path = os.path.dirname(clld.__file__) + "/web/templates/app.mako"
    clld_util_mako_path = os.path.dirname(clld.__file__) + "/web/templates/util.mako"
    project_templates_path = os.path.dirname(os.path.abspath(__file__)) + "/templates"
    project_app_mako_path = project_templates_path + "/app.mako"
    project_util_mako_path = project_templates_path + "/util.mako"

    if not os.path.exists(project_app_mako_path) or not filecmp.cmp(clld_app_mako_path, project_app_mako_path):
        copyfile(clld_app_mako_path, project_app_mako_path)
    if not os.path.exists(project_util_mako_path) or not filecmp.cmp(clld_util_mako_path, project_util_mako_path):
        copyfile(clld_util_mako_path, project_util_mako_path)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    sync_clld_mako()
    settings['route_patterns'] = {
        'contributions': '/inventories',
        'contribution': r'/inventories/view/{id:[^/\.]+}',
    }
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_route('faq', '/faq')
    config.add_route('conventions', '/conventions')

    config.include('clldmpg')
    config.registry.registerUtility(PhoibleMapMarker(), interfaces.IMapMarker)
    config.registry.registerUtility(PhoibleCtxFactoryQuery(), interfaces.ICtxFactoryQuery)
    config.add_static_view('data', 'phoible:static/data')
    # config.register_download(RdfDump(Dataset, 'phoible', description='RDF dump'))

    config.scan()
    return config.make_wsgi_app()
