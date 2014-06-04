from __future__ import unicode_literals
import sys
import unicodedata

from sqlalchemy.orm import joinedload, joinedload_all
import xlrd
from clld.scripts.util import (
    initializedb, Data, gbs_func, bibtex2source, glottocodes_by_isocode,
    add_language_codes,
)
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.dsv import reader
from clld.lib.bibtex import Database, Record
from clld.util import dict_append

from phoible import models
from phoible.scripts.util import coord, strip_quotes, language_name, SOURCES, BIB


def main(args):
    files_dir = args.data_file('files')
    if not files_dir.exists():
        files_dir.mkdir()
    data = Data()
    # TODO: get glottolog data
    glottocodes = glottocodes_by_isocode(args.glottolog_dburi)

    bib = Database.from_file(args.data_file('ALL.bib'), lowercase=True)
    refs = {}
    bibkeys = {}
    special_bib = [Record.from_string('@' + s, lowercase=True)
                   for s in filter(None, BIB.split('@'))]

    for row in reader(args.data_file('phoible_ids_bibtex.csv'), namedtuples=True):
        bibkeys[row.bibtex_key] = 1
        if row.bibtex_key == 'NO SOURCE GIVEN':
            refs[row.inventory_id] = []
        else:
            dict_append(refs, row.inventory_id, row.bibtex_key)

    dataset = data.add(
        common.Dataset, 'phoible',
        id='phoible',
        name='PHOIBLE Online',
        description='Phonetics Information Base Online',
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
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

    for row in reader(args.data_file('PHOIBLE_Aggregated_2155.tab'), namedtuples=True):
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
                population=0 if row.population in
                ['Extinct', 'No_known_speakers', 'No_estimate_available', 'Ancient']
                else int(row.population.replace(',', '')),
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

        DBSession.add(common.ContributionContributor(
            contribution=contrib, contributor=contributor))

    DBSession.flush()

    xls = xlrd.open_workbook(args.data_file('phonological_squibs', 'phonological_squibs_index.xlsx'))
    matrix = xls.sheet_by_name('Sheet1')
    for i in range(1, matrix.nrows):
        iid = str(int(matrix.cell(i, 0).value))

        if iid not in data['Inventory']:
            continue
        inventory = data['Inventory'][iid]
        src = matrix.cell(i, 1).value.strip()
        if src.startswith('http://'):
            inventory.source_url = src
        else:
            if not args.data_file('phonological_squibs', src).exists():
                print 'missing squib', src
            else:
                f = common.Contribution_files(
                    object=inventory,
                    id='%s-squib.pdf' % inventory.id,
                    name='Phonological squib',
                    mime_type='application/pdf')
                f.create(files_dir, file(args.data_file('phonological_squibs', src)).read())

    for rec in bib:
        if rec.id in bibkeys and rec.id not in data['Source']:
            data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    DBSession.flush()

    for row in reader(args.data_file('PHOIBLE_PhonemeLevel_2155.tab'), namedtuples=True):
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

    for i, row in enumerate(reader(args.data_file('unitvalues.tab'))):
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
    q = DBSession.query(common.Parameter).join(common.ValueSet).distinct()
    n = q.count()
    print n
    for segment in q:
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
