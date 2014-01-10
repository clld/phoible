from sqlalchemy import Integer
from sqlalchemy.sql.expression import cast

from clld.web.datatables.base import LinkCol, Col
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values, ValueSetCol
from clld.db.util import get_distinct_values, icontains
from clld.db.models.common import Contribution, ValueSet, Parameter


from phoible.models import Glyph


class ClassCol(Col):
    def __init__(self, dt, name, model_col, **kw):
        kw['model_col'] = model_col
        kw['choices'] = get_distinct_values(model_col)
        super(ClassCol, self).__init__(dt, name, **kw)


class Glyphs(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            ClassCol(self, 'segment_class', Glyph.segment_class),
            ClassCol(self, 'combined_class', Glyph.combined_class),
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


class Phonemes(Values):
    def col_defs(self):
        res = super(Phonemes, self).col_defs()
        if self.parameter:
            res[0] = InventoryCol(self, 'inventory')
        else:
            res = res[1:]
        if self.contribution:
            get_param = lambda item: item.valueset.parameter
            return [
                DatapointCol(self, 'valueset'),
                ClassCol(self, 'segment_class', Glyph.segment_class, get_obj=get_param),
                ClassCol(self, 'combined_class', Glyph.combined_class, get_obj=get_param)]
        return res

    def base_query(self, query):
        query = super(Phonemes, self).base_query(query)
        if self.parameter:
            query = query.join(ValueSet.contribution)
        return query
