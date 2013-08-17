from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Parameter


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.IParameter)
class Glyph(Parameter, CustomModelMixin):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    segment_class = Column(Unicode)  # consonant, ...
    combined_class = Column(Unicode)

    @property
    def number_of_combined_glyphs(self):
        return len(self.combined_class.split('-'))
