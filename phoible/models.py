from __future__ import unicode_literals

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
from clld.util import slug
from clld.lib.rdf import url_for_qname
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Parameter, Contribution, Language, Contributor, HasSourceMixin,
    IdNameDescriptionMixin,
)


class Genus(Base, IdNameDescriptionMixin):
    __wals_map__ = {
        'sumatra': 'northwestsumatrabarrierislands',
        'malayic': 'malayosumbawan',
        'southmindanao': 'bilic',
        'northwestmalayopolynesian': 'northborneo',
        'sundanese': 'malayosumbawan',
        #'transnewguinea': '',
        #'moklen': 'moklen',
        #'gayo': 'gayo',
    }
    gone = Column(Boolean, default=False)
    ficon = Column(String)
    gicon = Column(String)
    root = Column(String)

    def wals_url(self):
        wid = self.__wals_map__.get(self.id, self.id)
        return 'http://wals.info/languoid/genus/' + wid


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
#
# TODO: turn WALS genus into first class object, with icon spec!
#
@implementer(interfaces.ILanguage)
class Variety(Language, CustomModelMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

    country = Column(Unicode)
    area = Column(Unicode)
    population = Column(Integer)
    population_comment = Column(Unicode)
    count_inventories = Column(Integer)
    genus_pk = Column(Integer, ForeignKey('genus.pk'))
    genus = relationship(Genus, backref='languages')

    @property
    def wals_genus_url(self):
        if self.genus:
            return self.genus.wals_url()

    def __rdf__(self, request):
        if self.genus:
            yield 'skos:broader', self.wals_genus_url
        if self.country:
            yield 'dcterms:spatial', self.country


@implementer(interfaces.IParameter)
class Segment(Parameter, CustomModelMixin):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    segment_class = Column(Unicode)  # consonant, ...
    combined_class = Column(Unicode)

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
        #
        # TODO: features! something useful in GOLD?
        #http://purl.org/linguistics/gold/feature
        #http://purl.org/linguistics/gold/PhoneticProperty
        #for d in self.data:
        #    yield 'gold:feature', request.resource_url(self, _anchor=d.key)


@implementer(interfaces.IContribution)
class Inventory(Contribution, CustomModelMixin):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source = Column(String)
    source_url = Column(String)

    language_pk = Column(Integer, ForeignKey('language.pk'))
    language = relationship(Language, backref=backref('inventories'))
    count_tone = Column(Integer, default=0, nullable=False)
    count_vowel = Column(Integer, default=0, nullable=False)
    count_consonant = Column(Integer, default=0, nullable=False)

    @hybrid_property
    def count(self):
        return self.count_tone + self.count_consonant + self.count_vowel

    def __rdf__(self, request):
        if self.source_url:
            yield 'dcterms:related', self.source_url
        yield 'dcterms:about', request.resource_url(self.language)


class ContributorReference(Base, HasSourceMixin):
    contributor_pk = Column(Integer, ForeignKey('contributor.pk'))
    contributor = relationship(Contributor, backref='references')
