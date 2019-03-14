from zope.interface import implementer
from sqlalchemy import (
    Column,
    Boolean,
    String,
    Unicode,
    Integer,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.lib.rdf import url_for_qname
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Parameter, Contribution, Language, Contributor, HasSourceMixin, Value,
)
from clld_glottologfamily_plugin.models import HasFamilyMixin


# ----------------------------------------------------------------------------
# specialized common mapper classes
# ----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, HasFamilyMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

    count_inventories = Column(Integer)


@implementer(interfaces.IValue)
class Phoneme(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    allophones = Column(Unicode)
    marginal = Column(Boolean, nullable=True)


@implementer(interfaces.IParameter)
class Segment(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    segment_class = Column(Unicode)  # consonant, ...
    equivalence_class = Column(Unicode)

    in_inventories = Column(Integer)
    total_inventories = Column(Integer)
    frequency = Column(Float)

    @hybrid_property
    def representation(self):
        return float(self.in_inventories) / float(self.total_inventories)

    def __rdf__(self, request):
        cls = self.segment_class.capitalize() \
            if self.segment_class in ['consonant', 'vowel'] else 'Segment'
        yield 'rdf:type', url_for_qname('gold:' + cls)
        if self.segment_class:
            yield 'dcterms:description', self.segment_class


@implementer(interfaces.IContribution)
class Inventory(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source = Column(String)
    source_url = Column(String)
    internetarchive_url = Column(String)

    language_pk = Column(Integer, ForeignKey('language.pk'))
    language = relationship(Language, backref=backref('inventories'))
    count_tone = Column(Integer)
    count_vowel = Column(Integer, default=0, nullable=False)
    count_consonant = Column(Integer, default=0, nullable=False)

    @hybrid_property
    def count(self):
        return (self.count_tone or 0) + self.count_consonant + self.count_vowel

    def __rdf__(self, request):
        if self.source_url:
            yield 'dcterms:related', self.source_url
        yield 'dcterms:about', request.resource_url(self.language)
        for vs in self.valuesets:
            yield 'dcterms:hasPart', request.resource_url(vs)


class ContributorReference(Base, HasSourceMixin):
    contributor_pk = Column(Integer, ForeignKey('contributor.pk'))
    contributor = relationship(Contributor, backref='references')
