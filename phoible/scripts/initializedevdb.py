from __future__ import unicode_literals
import sys
from collections import defaultdict

from sqlalchemy import create_engine
from clld.scripts.util import initializedb, Data, gbs_func, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.dsv import rows
from clld.lib.bibtex import Database
from clld.util import dict_append

from phoible import models


DATA = {
    'bib': 'ALL.bib',
    'ref': 'phoible_ids_bibtex.csv',
    'aggregated': 'PHOIBLE_Aggregated_2155.tab',
    'phonemelevel': 'PHOIBLE_PhonemeLevel_2155.tab',
}
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


def language_name(s):
    s = s.split(';')[0].strip()
    if s.startswith('"'):
        s = s[1:]
    if s.endswith('"'):
        s = s[:-1]
    return s.capitalize()


def main(args):
    data = Data()
    glottocodes = {}

    bib = Database.from_file(args.data_file(DATA['bib']), lowercase=True)
    refs = {}
    bibkeys = {}

    for row in rows(args.data_file(DATA['ref']), namedtuples=True, encoding='utf8'):
        bibkeys[row.bibtex_key] = 1
        if row.bibtex_key == 'NO SOURCE GIVEN':
            refs[row.inventory_id] = []
        else:
            dict_append(refs, row.inventory_id, row.bibtex_key)

    dataset = data.add(
        common.Dataset, 'phoible',
        id='phoible',
        name='PHOIBLE',
        description='PHOnetics Information Base and LExicon Online',
        domain='phoible.org',
        license='http://creativecommons.org/licenses/by-sa/3.0/',
        contact='phoible@uw.edu',
        jsondata={
            'license_icon': 'http://i.creativecommons.org/l/by-sa/3.0/88x31.png',
            'license_name': 'Creative Commons Attribution-ShareAlike 3.0 Unported License'})

    for i, spec in enumerate([
        ('moran', "Steven Moran"),
        ('mccloy', "Daniel McCloy"),
        ('wright', "Richard Wright"),
    ]):
        DBSession.add(common.Editor(
            dataset=dataset,
            ord=i + 1,
            contributor=common.Contributor(id=spec[0], name=spec[1])))

    for row in rows(args.data_file(DATA['aggregated']), namedtuples=True, encoding='utf8'):
        if row.inventory_id not in refs:
            continue
        if row.language_code_id not in data['Language']:
            lang = data.add(
                common.Language, row.language_code_id,
                id=row.language_code_id,
                name=language_name(row.alternative_language_names),
                latitude=coord(row.latitude),
                longitude=coord(row.longitude))
            iso = data.add(
                common.Identifier, 'iso:%s' % lang.id,
                id=lang.id,
                name=lang.id,
                type=common.IdentifierType.iso.value)
            DBSession.add(common.LanguageIdentifier(language=lang, identifier=iso))

            if lang.id in glottocodes:
                code = data.add(
                    common.Identifier, 'glottolog:%s' % lang.id,
                    id=glottocodes[lang.id],
                    name=glottocodes[lang.id],
                    type=common.IdentifierType.glottolog.value)
                DBSession.add(common.LanguageIdentifier(language=lang, identifier=code))
        else:
            lang = data['Language'][row.language_code_id]

        if row.Source in data['Contributor']:
            contributor = data['Contributor'][row.Source]
        else:
            contributor = data.add(
                common.Contributor, row.Source,
                id=row.Source,
                name=row.Source)

        contrib = data.add(
            models.Inventory, row.inventory_id,
            id=row.inventory_id,
            language=lang,
            source=row.Source,
            name='%s %s (%s)' % (row.inventory_id, lang.name, row.Source))

        DBSession.add(common.ContributionContributor(contribution=contrib, contributor=contributor))

    DBSession.flush()

    for rec in bib:
        if rec.id not in bibkeys:
            continue
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    DBSession.flush()

    for row in rows(args.data_file(DATA['phonemelevel']), namedtuples=True, encoding='utf8'):
        if row.inventory_id not in refs:
            continue
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
            contribution=data['Inventory'][row.inventory_id],
            language=data['Language'][row.language_code_id],
            parameter=glyph)

        for ref in refs[row.inventory_id]:
            data.add(
                common.ValueSetReference, '%s-%s' % (vs.id, ref),
                source=data['Source'][ref],
                valueset=vs)

        data.add(
            common.Value, row.phoneme_id,
            id=row.phoneme_id,
            name='exists',
            valueset=vs)
        DBSession.flush()

    for inventory_id in refs:
        for ref in refs[inventory_id]:
            data.add(
                common.ContributionReference, '%s-%s' % (inventory_id, ref),
                source=data['Source'][ref],
                contribution=data['Inventory'][inventory_id])


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    #gbs_func('update', args)


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
