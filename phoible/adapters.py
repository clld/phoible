from zope.interface import implementer
from sqlalchemy.orm import joinedload

from clld import interfaces
from clld.lib import bibtex
from clld.web.adapters.geojson import GeoJsonParameterMultipleValueSets
from clld.web.adapters.cldf import CldfConfig
from clld.web.adapters import md
from clld.db.models.common import ValueSet

from phoible.models import Variety


class PhoibleCldfConfig(CldfConfig):
    module = 'StructureDataset'


class GeoJsonFeature(GeoJsonParameterMultipleValueSets):
    def get_query(self, ctx, req):
        query = GeoJsonParameterMultipleValueSets.get_query(self, ctx, req)
        return query.options(joinedload(ValueSet.language).joinedload(Variety.family))


class MetadataFromRec(md.Metadata):
    def rec(self, ctx, req):
        return bibtex.Record(
            'inbook',
            '%s-%s' % (req.dataset.id, ctx.id),
            url=req.resource_url(ctx),
            address=req.dataset.publisher_place,
            publisher=req.dataset.publisher_name,
            year=str(req.dataset.published.year),
            title='%s sound inventory (%s)' % (
                ctx.language.name, ctx.primary_contributors[0].id),
            author=ctx.primary_contributors[0].name.split(' and '),
            booktitle=req.dataset.description,
            editor=[c.contributor.name for c in list(req.dataset.editors)])


@implementer(interfaces.IRepresentation, interfaces.IMetadata)
class BibTex(MetadataFromRec):
    """Resource metadata as BibTex record.
    """
    name = 'BibTeX'
    __label__ = 'BibTeX'
    unapi = 'bibtex'
    extension = 'md.bib'
    mimetype = 'text/x-bibtex'

    def render(self, ctx, req):
        return str(self.rec(ctx, req))


@implementer(interfaces.IRepresentation, interfaces.IMetadata)
class ReferenceManager(MetadataFromRec):
    """Resource metadata in RIS format.
    """
    name = 'RIS'
    __label__ = 'RIS'
    unapi = 'ris'
    extension = 'md.ris'
    mimetype = "application/x-research-info-systems"

    def render(self, ctx, req):
        return self.rec(ctx, req).format('ris')


@implementer(interfaces.IRepresentation, interfaces.IMetadata)
class TxtCitation(md.Metadata):
    """Resource metadata formatted as plain text citation.
    """
    name = "Citation"
    __label__ = 'Text'
    extension = 'md.txt'
    mimetype = 'text/plain'
    template = 'contribution/md_txt.mako'


def includeme(config):
    config.register_adapter(GeoJsonFeature, interfaces.IParameter)
    config.registry.registerUtility(PhoibleCldfConfig(), interfaces.ICldfConfig)

    for cls in [BibTex, TxtCitation, ReferenceManager]:
        for if_ in [interfaces.IRepresentation, interfaces.IMetadata]:
            config.register_adapter(cls, interfaces.IContribution, if_)
