from sqlalchemy import Integer
from sqlalchemy.sql.expression import cast

from clld.web.datatables.base import LinkCol, Col
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values, ValueSetCol
from clld.db.util import get_distinct_values, icontains
from clld.db.models.common import Contribution, ValueSet, Parameter


from phoible.models import Glyph


class SegmentClassCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = get_distinct_values(Glyph.segment_class)
        super(SegmentClassCol, self).__init__(dt, name, **kw)


class CombinedClassCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = get_distinct_values(Glyph.combined_class)
        super(CombinedClassCol, self).__init__(dt, name, **kw)


class Glyphs(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            SegmentClassCol(self, 'segment_class', model_col=Glyph.segment_class),
            CombinedClassCol(self, 'combined_class', model_col=Glyph.combined_class),
        ]


class InventoryCol(LinkCol):
    def get_obj(self, item):
        return item.valueset.contribution

    def search(self, qs):
        return icontains(Contribution.name, qs)

    def order(self):
        return cast(Contribution.id, Integer)


class DatapointCol(ValueSetCol):
    def get_attrs(self, item):
        return {'label': item.valueset.parameter.name}

    def search(self, qs):
        return icontains(Parameter.name, qs)

    def order(self):
        return Parameter.id


class _SegmentClassCol(SegmentClassCol):
    def format(self, item):
        return item.valueset.parameter.segment_class

    def search(self, qs):
        return Glyph.segment_class.__eq__(qs)

    def order(self):
        return Glyph.segment_class


class _CombinedClassCol(CombinedClassCol):
    def format(self, item):
        return item.valueset.parameter.combined_class

    def search(self, qs):
        return Glyph.combined_class.__eq__(qs)

    def order(self):
        return Glyph.combined_class


class Phonemes(Values):
    def col_defs(self):
        res = super(Phonemes, self).col_defs()
        if self.parameter:
            res[0] = InventoryCol(self, 'inventory')
        else:
            res = res[1:]
        if self.contribution:
            return [
                DatapointCol(self, 'valueset'),
                _SegmentClassCol(self, 'segment_class'),
                _CombinedClassCol(self, 'combined_class')]
        return res

    def base_query(self, query):
        query = super(Phonemes, self).base_query(query)
        if self.parameter:
            query = query.join(ValueSet.contribution)
        return query
