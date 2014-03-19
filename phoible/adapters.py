from zope.interface import implementer

from clld import interfaces
from clld.lib import bibtex
from clld.web.adapters.geojson import GeoJsonParameter
from clld.web.adapters import md


class GeoJsonFeature(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        return {}


class MetadataFromRec(md.Metadata):
    def rec(self, ctx, req):
        data = {}
        if interfaces.IContribution.providedBy(ctx):
            genre = 'inbook'
            data['title'] = '%s sound inventory (%s)' % (ctx.language.name, ctx.primary_contributors[0].id)
            data['author'] = ctx.primary_contributors[0].description.split(' and ')
            data['booktitle'] = req.dataset.description
            data['editor'] = [c.contributor.name for c in list(req.dataset.editors)]
            id_ = '%s-%s' % (req.dataset.id, ctx.id)
        else:
            genre = 'book'
            data['editor'] = [c.contributor.name for c in list(ctx.editors)]
            id_ = req.dataset.id
            data['title'] = getattr(ctx, 'citation_name', ctx.__unicode__())

        return bibtex.Record(
            genre,
            id_,
            url=req.resource_url(ctx),
            address=req.dataset.publisher_place,
            publisher=req.dataset.publisher_name,
            year=str(req.dataset.published.year),
            **data)


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
        return self.rec(ctx, req).__unicode__()


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

    def render(self, ctx, req):
        if interfaces.IContribution.providedBy(ctx):
            self.template = 'contribution/md_txt.mako'
        else:  # if interfaces.IDataset.providedBy(ctx):
            self.template = 'dataset/md_txt.mako'
        return super(TxtCitation, self).render(ctx, req)


def includeme(config):
    config.register_adapter(GeoJsonFeature, interfaces.IParameter)

    for cls in [BibTex, TxtCitation, ReferenceManager]:
        for if_ in [interfaces.IRepresentation, interfaces.IMetadata]:
            config.register_adapter(cls, interfaces.IContribution, if_)
