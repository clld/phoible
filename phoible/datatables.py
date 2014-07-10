from sqlalchemy import Integer
from sqlalchemy.sql.expression import cast

from clld.web.datatables.base import LinkCol, Col, PercentCol, filter_number, LinkToMapCol
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values, RefsCol
from clld.web.datatables.contribution import Contributions, ContributorsCol, CitationCol
from clld.web.util.helpers import external_link, map_marker_img
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.util import get_distinct_values, icontains
from clld.db.models.common import (
    Contribution, ValueSet, Parameter, Contributor, ContributionContributor, Language,
)


from phoible.models import Segment, Variety, Inventory, Genus


class FamilyCol(Col):
    __kw__ = dict(sTitle='WALS family')

    def format(self, item):
        return HTML.span(
            map_marker_img(self.dt.req, item),
            ' ',
            item.genus.description if item.genus else '',
        )

    def order(self):
        return Genus.description

    def search(self, qs):
        return icontains(Genus.description, qs)


class GenusCol(Col):
    __kw__ = dict(sTitle='WALS genus')

    def format(self, item):
        if not item.genus:
            return ''
        return external_link(item.wals_genus_url, label=item.genus.name)

    def order(self):
        return Genus.name

    def search(self, qs):
        return icontains(Genus.name, qs)


class Varieties(Languages):
    def base_query(self, query):
        return query.outerjoin(Genus)

    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self,
                '#',
                bSearchable=False,
                sDescription='Number of inventories',
                model_col=Variety.count_inventories),
            GenusCol(self, 'WALS genus'),
            FamilyCol(self, 'WALS family'),
            Col(self, 'latitude'),
            Col(self, 'longitude'),
            Col(self, 'country', model_col=Variety.country),
            Col(self, 'area',
                model_col=Variety.area,
                choices=get_distinct_values(Variety.area)),
            Col(self, 'population', model_col=Variety.population),
        ]


class ClassCol(Col):
    def __init__(self, dt, name, model_col, **kw):
        kw['model_col'] = model_col
        kw['choices'] = get_distinct_values(model_col)
        super(ClassCol, self).__init__(dt, name, **kw)


class DescCol(LinkCol):
    def get_attrs(self, item):
        return {'label': item.description}


class FrequencyCol(Col):
    __kw__ = {'sClass': 'right', 'sTitle': 'Representation'}

    def format(self, item):
        segment = self.get_obj(item)
        return '%s/%s (%.0f%%)' % (
            segment.in_inventories,
            segment.total_inventories,
            segment.representation * 100)

    def search(self, qs):
        return filter_number(Segment.in_inventories, qs)

    def order(self):
        return Segment.in_inventories


class Segments(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            FrequencyCol(self, 'frequency'),
            DescCol(self, 'description'),
            ClassCol(self, 'segment_class', Segment.segment_class),
            ClassCol(self, 'combined_class', Segment.combined_class),
        ]

    def get_options(self):
        opts = super(Segments, self).get_options()
        opts['aaSorting'] = [[1, 'desc']]
        return opts


class InventoryCol(LinkCol):
    def get_obj(self, item):
        return item.valueset.contribution

    def search(self, qs):
        return icontains(Contribution.name, qs)

    def order(self):
        return cast(Contribution.id, Integer)


class DatapointCol(LinkCol):
    __kw__ = {'sTitle': 'Segment'}

    def get_obj(self, item):
        return item.valueset.parameter

    def search(self, qs):
        return icontains(Parameter.name, qs)

    def order(self):
        return Parameter.id


class Phonemes(Values):
    def get_options(self):
        opts = super(Values, self).get_options()
        if self.contribution:
            opts['aaSorting'] = [[1, 'desc'], [0, 'asc']]
        return opts

    def col_defs(self):
        if self.parameter:
            return [
                InventoryCol(self, 'inventory'),
                LinkCol(self,
                        'language',
                        model_col=Language.name,
                        get_object=lambda i: i.valueset.language),
                RefsCol(self, 'source'),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
            ]

        res = super(Phonemes, self).col_defs()[1:]
        if self.contribution:
            param = lambda item: item.valueset.parameter
            return [
                DatapointCol(self, 'valueset'),
                FrequencyCol(self, 'frequency', get_object=param),
                ClassCol(
                    self, 'segment_class', Segment.segment_class, get_object=param),
                ClassCol(
                    self, 'combined_class', Segment.combined_class, get_object=param)]
        return res  # pragma: no cover

    def base_query(self, query):
        query = super(Phonemes, self).base_query(query)
        if self.parameter:
            query = query.join(ValueSet.contribution)
        return query


class CountCol(Col):
    __kw__ = dict(sClass='right', sTitle='# segments')

    def format(self, item):
        return item.count

    def order(self):
        return Inventory.count

    def search(self, qs):
        return filter_number(Inventory.count, qs, type_=int)


class PhoibleContributorsCol(ContributorsCol):
    __kw__ = {}

    def __init__(self, dt, name, **kw):
        kw['choices'] = [c.name for c in
                         DBSession.query(Contributor).join(ContributionContributor)]
        super(PhoibleContributorsCol, self).__init__(dt, name, **kw)

    def order(self):
        return Contributor.name

    def search(self, qs):
        return icontains(Contributor.name, qs)


class Inventories(Contributions):
    def base_query(self, query):
        return query.join(ContributionContributor).join(Contributor).distinct()

    def col_defs(self):
        res = [LinkCol(self, 'name'), CountCol(self, 'all')]
        for c in 'vowel consonant tone'.split():
            res.append(Col(
                self, c, model_col=getattr(Inventory, 'count_' + c), sTitle='# %ss' % c))
        res.extend([
            PhoibleContributorsCol(self, 'contributor'),
            CitationCol(self, 'cite'),
        ])
        return res


def includeme(config):
    config.register_datatable('languages', Varieties)
    config.register_datatable('parameters', Segments)
    config.register_datatable('values', Phonemes)
    config.register_datatable('contributions', Inventories)

