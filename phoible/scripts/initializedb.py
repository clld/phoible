from __future__ import unicode_literals
import sys
import transaction

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.dsv import rows

from phoible import models


def coord(s):
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
    for row in rows(args.data_file('PHOIBLE_Aggregated_1601.tab'), namedtuples=True, encoding='utf8'):
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
    glyph_names = {}
    for row in rows(args.data_file('PHOIBLE_PhonemeLevel_1601.tab'), namedtuples=True, encoding='utf8'):
        if row.glyph_id not in data['Glyph']:
            name = '%s (%s)' % (row.glyph, row.Source)
            if name in glyph_names:
            #    name = name = '%s (%s)' % (name, row.Source)
                for i in range(1, 10):
                    name = '%s [%s]' % (name, i)
                    if name not in glyph_names:
                        break
            glyph_names[name] = 1
            glyph = data.add(
                models.Glyph, row.glyph_id,
                id=row.glyph_id,
                name=name,
                segment_class=row.class_,
                combined_class=row.CombinedClass)
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


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
