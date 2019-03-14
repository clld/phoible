from sqlalchemy import Integer
from sqlalchemy.sql.expression import cast
from sqlalchemy.orm import joinedload_all, joinedload

from clld.web.datatables.base import LinkCol, Col, filter_number, LinkToMapCol, RefsCol as BaseRefsCol
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values, RefsCol
from clld.web.datatables.contribution import Contributions, ContributorsCol, CitationCol
from clld.web.datatables.contributor import Contributors
from clld.web.util.helpers import maybe_external_link
from clld.db.meta import DBSession
from clld.db.util import get_distinct_values, icontains
from clld.db.models.common import (
    Contribution, ValueSet, Parameter, Contributor, ContributionContributor, Language,
    Value,
)
from clld_glottologfamily_plugin.datatables import FamilyCol


from phoible.models import Segment, Variety, Inventory, Phoneme



class Varieties(Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self,
                '#',
                bSearchable=False,
                sDescription='Number of inventories',
                model_col=Variety.count_inventories),
            FamilyCol(self, 'family', Variety),
            Col(self, 'latitude'),
            Col(self, 'longitude'),
            Col(self, 'macroarea',
                model_col=Variety.macroarea,
                choices=get_distinct_values(Variety.macroarea)),
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
        return '%s (%.0f%%)' % (segment.in_inventories, segment.representation * 100)

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
            opts['aaSorting'] = [[4, 'desc'], [1, 'asc']]
        return opts

    def col_defs(self):
        if self.parameter:
            return [
                InventoryCol(self, 'inventory'),
                Col(self, 'marginal', model_col=Phoneme.marginal),
                Col(self, 'allophones', model_col=Phoneme.allophones),
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
                ClassCol(self, 'segment_class', Segment.segment_class, get_object=param),
                DatapointCol(self, 'valueset'),
                Col(self, 'marginal', model_col=Phoneme.marginal),
                Col(self, 'allophones', model_col=Phoneme.allophones),
                FrequencyCol(self, 'frequency', get_object=param),
            ]
        return res

    def base_query(self, query):
        query = super(Phonemes, self).base_query(query)
        if self.parameter:
            query = query.join(ValueSet.contribution).options(
                joinedload_all(Value.valueset, ValueSet.language),
                joinedload_all(Value.valueset, ValueSet.contribution))
        return query


class CountCol(Col):
    __kw__ = dict(sClass='right', sTitle='# segments')

    def format(self, item):
        return item.count


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


class LanguageCol(LinkCol):
    def get_obj(self, item):
        return item.language

    def order(self):
        return Language.name

    def search(self, qs):
        return icontains(Language.name, qs)


class Inventories(Contributions):
    def base_query(self, query):
        return query\
            .join(ContributionContributor)\
            .join(Contributor)\
            .join(Language)\
            .distinct()\
            .options(
                joinedload(Contribution.contributor_assocs).joinedload(ContributionContributor.contributor),
                joinedload(Inventory.language),
        )

    def col_defs(self):
        res = [
            LinkCol(self, 'name', sTitle='Inventory'),
            LanguageCol(self, 'language'),
            CountCol(self, 'all', bSearchable=False, bSortable=False)]
        for c in 'vowel consonant tone'.split():
            res.append(Col(
                self, c, model_col=getattr(Inventory, 'count_' + c), sTitle='# %ss' % c))
        res.extend([
            PhoibleContributorsCol(self, 'contributor'),
            CitationCol(self, 'cite'),
        ])
        return res


class InventorySources(Contributors):
    def base_query(self, query):
        return query.filter(Contributor.id != 'mccloy')

    def col_defs(self):
        return [
            LinkCol(self, 'contributor'),
            Col(self, 'description'),
            BaseRefsCol(self, 'sources'),
            Col(self, 'url', format=lambda i: maybe_external_link(i.url)),
        ]


def includeme(config):
    config.register_datatable('languages', Varieties)
    config.register_datatable('parameters', Segments)
    config.register_datatable('values', Phonemes)
    config.register_datatable('contributors', InventorySources)
    config.register_datatable('contributions', Inventories)
