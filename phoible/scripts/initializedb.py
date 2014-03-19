from __future__ import unicode_literals
import sys
from getpass import getuser
import unicodedata

from sqlalchemy.orm import joinedload, joinedload_all
from clld.scripts.util import (
    initializedb, Data, gbs_func, bibtex2source, glottocodes_by_isocode,
    add_language_codes,
)
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.dsv import rows
from clld.lib.bibtex import Database, Record
from clld.util import dict_append

from phoible import models


SOURCES = {
    'AA': ('C. Chanard and Rhonda L. Hartell',
           ['Hartell1993', 'Chanard2006'],
           'Chanard and Hartell'),
    'PHOIBLE': ('Phonetics Information Base and Lexicon',
                ['Moran2012a'],
                'Steven Moran'),
    'SPA': ('Stanford Phonology Archive',
            ['SPA1979'],
            'John H. Crothers et al.'),
    'UPSID': ('UCLA Phonological Segment Inventory Database',
              ['Maddieson1984', 'MaddiesonPrecoda1990'],
              'Ian Maddieson and Kristin Precoda')}

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


def strip_quotes(s):
    s = s.strip()
    if s.startswith('"'):
        s = s[1:]
    if s.endswith('"'):
        s = s[:-1]
    return s


def language_name(s):
    s = strip_quotes(s.split(';')[0])
    for sep in ['-', ' ', '(']:
        if sep in s:
            s = sep.join(ss.capitalize() for ss in s.split(sep))
    return s.capitalize()


def main(args):
    data = Data()

    glottocodes = {}
    if getuser() == 'robert':
        glottocodes = glottocodes_by_isocode('postgresql://robert@/glottolog3')

    bib = Database.from_file(args.data_file('ALL.bib'), lowercase=True)
    refs = {}
    bibkeys = {}

    special_bib = """\
@book{Hayes2009,
        Author = {Bruce Hayes},
        Publisher = {Blackwell},
        Timestamp = {2010.08.08},
        Title = {Introductory Phonology},
        Year = {2009}
}
@inproceedings{MoisikEsling2011,
        title={The 'whole larynx' approach to laryngeal features},
        author={Moisik, Scott R. and Esling, John H.},
        booktitle={Proceedings of the International Congress of Phonetic Sciences (ICPhS XVII)},
        year={2011},
        pages={1406-1409}
}
@misc{Chanard2006,
        Author = {C. Chanard},
        Title = {Syst{\\`e}mes Alphab{\\'e}tiques Des Langues Africaines},
        Year = {2006},
        Url = {http://sumale.vjf.cnrs.fr/phono/}
}
@misc{SPA1979,
        Author = {John H. Crothers and James P. Lorentz and Donald A. Sherman and Marilyn M. Vihman},
        Title = {Handbook of Phonological Data From a Sample of the World's Languages: A Report of the Stanford Phonology Archive},
        Year = {1979}
}
@book{Hartell1993,
        Editor = {Hartell, Rhonda L.},
        Publisher = {UNESCO and Soci{\\'e}t{\\'e} Internationale de Linguistique},
        Title = {Alphabets des langues africaines},
        Year = {1993}
}
@book{Maddieson1984,
        Address = {Cambridge, UK},
        Author = {Maddieson, Ian},
        Publisher = {Cambridge University Press},
        Title = {Pattern of Sounds},
        Year = {1984}
}
@incollection{MaddiesonPrecoda1990,
        Author = {Ian Maddieson and Kristin Precoda},
        Booktitle = {UCLA Working Papers in Phonetics},
        Pages = {104--111},
        Publisher = {Department of Linguistics, UCLA},
        Title = {Updating UPSID},
        Volume = {74},
        Year = {1990}
}
@phdthesis{Moran2012a,
        Author = {Steven Moran},
        School = {University of Washington},
        Title = {Phonetics Information Base and Lexicon},
        Url = {https://digital.lib.washington.edu/researchworks/handle/1773/22452}
        Year = {2012}
}
    """
    special_bib = [Record.from_string('@' + s, lowercase=True)
                   for s in filter(None, special_bib.split('@'))]

    for row in rows(args.data_file('phoible_ids_bibtex.csv'), namedtuples=True, encoding='utf8'):
        bibkeys[row.bibtex_key] = 1
        if row.bibtex_key == 'NO SOURCE GIVEN':
            refs[row.inventory_id] = []
        else:
            dict_append(refs, row.inventory_id, row.bibtex_key)

    dataset = data.add(
        common.Dataset, 'phoible',
        id='phoible',
        name='PHOIBLE',
        description='Phonetics Information Base and Lexicon Online',
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

    for rec in special_bib:
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    for row in rows(args.data_file('PHOIBLE_Aggregated_2155.tab'), namedtuples=True, encoding='utf8'):
        if row.inventory_id not in refs:
            continue
        if row.language_code_id not in data['Variety']:
            lang = data.add(
                models.Variety, row.language_code_id,
                id=row.language_code_id,
                name=language_name(row.alternative_language_names),
                wals_genus=strip_quotes(row.wals_genus),
                country=strip_quotes(row.country),
                area=strip_quotes(row.area),
                population=0 if row.population in ['Extinct', 'No_known_speakers', 'No_estimate_available', 'Ancient'] else int(row.population.replace(',', '')),
                population_comment=row.population.replace('_', ' '),
                latitude=coord(row.latitude),
                longitude=coord(row.longitude))
            add_language_codes(data, lang, lang.id, glottocodes=glottocodes)
            #
            # TODO: add alternative names!
            #for name in row.alternative_language_names.split(';'):
            #    if name.strip() != lang.name:
            #        pass
        else:
            lang = data['Variety'][row.language_code_id]

        source = 'AA' if row.Source == 'Chanard' else row.Source
        if source in data['Contributor']:
            contributor = data['Contributor'][source]
        else:
            contributor = data.add(
                common.Contributor, source,
                id=source,
                name=SOURCES[source][0],
                description=SOURCES[source][2])
            for ref in SOURCES[source][1]:
                DBSession.add(models.ContributorReference(
                    source=data['Source'][ref], contributor=contributor))

        contrib = data.add(
            models.Inventory, row.inventory_id,
            id=row.inventory_id,
            language=lang,
            source=source,
            name='%s %s (%s)' % (row.inventory_id, lang.name, row.Source))

        DBSession.add(common.ContributionContributor(contribution=contrib, contributor=contributor))

    DBSession.flush()

    for rec in bib:
        if rec.id in bibkeys and rec.id not in data['Source']:
            data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    DBSession.flush()

    for row in rows(args.data_file('PHOIBLE_PhonemeLevel_2155.tab'), namedtuples=True, encoding='utf8'):
        if row.inventory_id not in refs:
            continue
        if row.glyph not in data['Segment']:
            segment = data.add(
                models.Segment, row.glyph,
                id=row.glyph_id,
                name=row.glyph,
                description=' - '.join(unicodedata.name(c) for c in row.glyph),
                segment_class=row.class_,
                combined_class=row.CombinedClass)
            DBSession.flush()
        else:
            segment = data['Segment'][row.glyph]

        vs = data.add(
            common.ValueSet, row.phoneme_id,
            id=row.phoneme_id,
            contribution=data['Inventory'][row.inventory_id],
            language=data['Variety'][row.language_code_id],
            parameter=segment)

        for ref in refs[row.inventory_id]:
            data.add(
                common.ValueSetReference, '%s-%s' % (vs.id, ref),
                source=data['Source'][ref],
                valueset=vs)

        data.add(
            common.Value, row.phoneme_id,
            id=row.phoneme_id,
            name='%s %s' % (row.glyph, data['Inventory'][row.inventory_id].name),
            valueset=vs)
        DBSession.flush()

    for inventory_id in refs:
        for ref in refs[inventory_id]:
            data.add(
                common.ContributionReference, '%s-%s' % (inventory_id, ref),
                source=data['Source'][ref],
                contribution=data['Inventory'][inventory_id])

    for i, row in enumerate(rows(args.data_file('unitvalues.tab'), encoding='utf8')):
        if i == 0:
            features = row
            continue

        if row[0] not in data['Segment']:
            #print row[0]
            continue
        for j, value in enumerate(row):
            if j and value != '0':
                DBSession.add(common.Parameter_data(
                    key=features[j],
                    value=value,
                    ord=j,
                    object_pk=data['Segment'][row[0]].pk))
    DBSession.flush()


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    q = DBSession.query(common.Parameter)
    n = q.count()
    for segment in q.options(joinedload(common.Parameter.valuesets)):
        segment.frequency = float(len(segment.valuesets)) / float(n)

    for inventory in DBSession.query(models.Inventory).options(
            joinedload_all(common.Contribution.valuesets, common.ValueSet.parameter)
    ):
        for vs in inventory.valuesets:
            attr = 'count_' + vs.parameter.segment_class
            if hasattr(inventory, attr):
                val = getattr(inventory, attr) or 0
                setattr(inventory, attr, val + 1)


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
