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
from clld.db.models.common import (
    Parameter, Value, Unit, Contribution, Language, Contributor, Source, HasSourceMixin,
)


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.IParameter)
class Glyph(Parameter, CustomModelMixin):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    segment_class = Column(Unicode)  # consonant, ...
    combined_class = Column(Unicode)


@implementer(interfaces.IContribution)
class Inventory(Contribution, CustomModelMixin):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source = Column(String)

    language_pk = Column(Integer, ForeignKey('language.pk'))
    language = relationship(Language, backref=backref('inventories'))


@implementer(interfaces.IUnit)
class Phoneme(Unit, CustomModelMixin):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)

    glyph_pk = Column(Integer, ForeignKey('glyph.pk'))
    glyph = relationship(Glyph, backref=backref('phoneme', uselist=False))

    #inventory_pk = Column(Integer, ForeignKey('inventory.pk'))
    #inventory = relationship(Inventory, backref=backref('phonemes'))


class ContributorReference(Base, HasSourceMixin):
    contributor_pk = Column(Integer, ForeignKey('contributor.pk'))
    contributor = relationship(Contributor, backref='references')
