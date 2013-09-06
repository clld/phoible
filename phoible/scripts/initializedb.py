from __future__ import unicode_literals
import sys
import transaction
from collections import defaultdict

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.dsv import rows
from clld.lib.bibtex import Database
from glottolog3.lib.bibtex import unescape

from phoible import models


SOURCES = ['AA', 'PHOIBLE', 'SPA', 'UPSID']
BIBS = {}


def coord(s):
    if s.endswith('-00'):
        s = s[:-3]

    if not ':' in s:
        return
    s = s.replace('`N', '')
    deg, min_ = s.split(':')

    def strip_leading_zeros(ss):
        while ss.startswith('0'):
            ss = ss[1:]
        return ss

    try:
        return float(strip_leading_zeros(deg) or 0) + float(strip_leading_zeros(min_) or 0) / 60.0
    except Exception:
        print s
        raise


def main(args):
    data = Data()

    #for src in SOURCES:
    #    BIBS[src] = Database.from_file(args.data_file('%s.bib' % src))

    bib = Database.from_file(args.data_file('ALL.bib'))
    refs = {}

    for lid, lname, src, key, year in rows(args.data_file('ALL_CODES_BIBTEX_KEYS.tab'), encoding='utf8'):
        if key in bib.keymap:
            k = (lid, src)
            if k in refs:
                refs[k].append(key)
            else:
                refs[k] = [key]
            #print '++++', src, key
        else:
            print '----', src, key

    data.add(
        common.Dataset, 'phoible',
        id='phoible',
        name='Phoible',
        description='PHOnetics Information Base and LExicon',
        domain='phoible.org',
        license='http://creativecommons.org/licenses/by-sa/3.0/',
        contact='steven.moran@uzh.ch',
        jsondata={
            'license_icon': 'http://i.creativecommons.org/l/by-sa/3.0/88x31.png',
            'license_name': 'Creative Commons Attribution-ShareAlike 3.0 Unported License'})

    """
        "ReportDate",
        "Source",
        "inventory_id",
        "language_code_id",
        "alternative_language_names",
        "SourceTrumpOrdering",
        "root",
        "wals_genus",
        "country",
        "area",
        "population",
        "latitude",
        "longitude",
        "phonemes",
        "TopLevel_consonant",
        "TopLevel_tone",
        "TopLevel_vowel",
    """
    for row in rows(args.data_file('PHOIBLE_Aggregated_2155.tab'), namedtuples=True, encoding='utf8'):
        if row.language_code_id not in data['Language']:
            data.add(
                common.Language, row.language_code_id,
                id=row.language_code_id,
                name=row.alternative_language_names,
                latitude=coord(row.latitude),
                longitude=coord(row.longitude))

        data.add(
            common.Contribution, row.inventory_id,
            id=row.inventory_id,
            name='%s %s (%s)' % (row.inventory_id, row.alternative_language_names, row.Source))

    DBSession.flush()

    for rec in bib:
        year = rec.get('Year', 'nd')
        if year.endswith('}'):
            year = year[:-1]
        data.add(
            common.Source, rec.id,
            id=rec.id,
            name=('%s %s' % (rec.get('Author', ''), year)).strip(),
            description=unescape(rec.get('Title', '')))

    DBSession.flush()

    for lid, src in refs:
        for key in set(refs[(lid, src)]):
            if lid in data['Language']:
                data['Language'][lid].sources.append(data['Source'][key])
            else:
                print lid, '--- missing language'

    """
    ReportDate
    Source
    inventory_id
    language_code_id
    alternative_language_names
    SourceTrumpOrdering
    root
    wals_genus
    country
    area
    population
    latitude
    longitude
    phoneme_id
    glyph_id
    glyph
    class
    CombinedClass
    NumOfCombinedGlyphs
    """
    for row in rows(args.data_file('PHOIBLE_PhonemeLevel_2155.tab'), namedtuples=True, encoding='utf8'):
        if row.glyph_id not in data['Glyph']:
            glyph = data.add(
                models.Glyph, row.glyph_id,
                id=row.glyph_id,
                name=row.glyph,
                segment_class=row.class_,
                combined_class=row.CombinedClass)
            DBSession.flush()
            data.add(
                models.Phoneme, row.glyph,
                id=row.glyph_id,
                glyph=glyph,
                name=row.glyph)
            DBSession.flush()
        else:
            glyph = data['Glyph'][row.glyph_id]

        vs = data.add(
            common.ValueSet, row.phoneme_id,
            id=row.phoneme_id,
            contribution=data['Contribution'][row.inventory_id],
            language=data['Language'][row.language_code_id],
            parameter=glyph)
        data.add(
            common.Value, row.phoneme_id,
            id=row.phoneme_id,
            name='exists',
            valueset=vs)
        DBSession.flush()

    unitdomains = {}
    for i, row in enumerate(rows(args.data_file('unitvalues.tab'), encoding='utf8')):
        for j, value in enumerate(row):
            if j:
                if i == 0:
                    unitdomains[j] = {}
                else:
                    if j in unitdomains:
                        unitdomains[j][value] = 1

    for i, row in enumerate(rows(args.data_file('unitvalues.tab'), encoding='utf8')):
        if i == 0:
            for j, name in enumerate(row):
                if j:
                    p = data.add(common.UnitParameter, j, id=str(j), name=name)
                    for k, de in enumerate(sorted(unitdomains[j].keys())):
                        data.add(
                            common.UnitDomainElement, '%s%s' % (j, de),
                            id='%s-%s' % (j, k + 1), name=de, parameter=p)

            DBSession.flush()
        else:
            if row[0] not in data['Phoneme']:
                print row[0]
                continue
            for j, value in enumerate(row):
                if j:
                    if value == '0':
                        continue
                    if j not in data['UnitParameter']:
                        continue
                    data.add(
                        common.UnitValue, '%s-%s' % (i, j),
                        id='%s-%s' % (i, j),
                        unitparameter=data['UnitParameter'][j],
                        #contribution=,
                        unitdomainelement=data['UnitDomainElement']['%s%s' % (j, value)],
                        name=value,
                        unit=data['Phoneme'][row[0]])
    DBSession.flush()


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
