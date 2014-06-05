from sqlalchemy import Integer
from sqlalchemy.sql.expression import cast

from clld.web.datatables.base import LinkCol, Col, PercentCol, filter_number
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values, ValueSetCol
from clld.web.datatables.contribution import Contributions, ContributorsCol, CitationCol
from clld.web.util.helpers import external_link
from clld.db.meta import DBSession
from clld.db.util import get_distinct_values, icontains
from clld.db.models.common import (
    Contribution, ValueSet, Parameter, Contributor, ContributionContributor,
)


from phoible.models import Segment, Variety, Inventory


class GenusCol(Col):
    __kw__ = dict(sTitle='WALS genus')

    def format(self, item):
        if not item.wals_genus:
            return ''
        return external_link(item.wals_genus_url, label=item.wals_genus)


class Varieties(Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            GenusCol(self, 'WALS genus', model_col=Variety.wals_genus),
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


class Segments(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            PercentCol(self, 'frequency', model_col=Segment.frequency),
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
    def col_defs(self):
        res = super(Phonemes, self).col_defs()
        if self.parameter:
            res[0] = InventoryCol(self, 'inventory')
        else:
            res = res[1:]
        if self.contribution:
            param = lambda item: item.valueset.parameter
            return [
                DatapointCol(self, 'valueset'),
                PercentCol(
                    self, 'frequency', model_col=Segment.frequency, get_object=param),
                ClassCol(
                    self, 'segment_class', Segment.segment_class, get_object=param),
                ClassCol(
                    self, 'combined_class', Segment.combined_class, get_object=param)]
        return res

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
        return filter_number(Inventory.col, qs, type_=int)


class PhoibleContributorsCol(ContributorsCol):
    __kw__ = {}

    def __init__(self, dt, name, **kw):
        kw['choices'] = [c.name for c in DBSession.query(Contributor).join(ContributionContributor)]
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

