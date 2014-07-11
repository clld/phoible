from __future__ import unicode_literals, print_function
import sys
import unicodedata
from itertools import groupby, cycle
from collections import defaultdict

from sqlalchemy.orm import joinedload, joinedload_all
from clld.scripts.util import (
    initializedb, Data, gbs_func, glottocodes_by_isocode, add_language_codes,
)
from clld.scripts.internetarchive import ia_func
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.dsv import reader
from clld.util import slug
from clld.web.icon import ORDERED_ICONS

from phoible import models
from phoible.scripts.util import (
    coord, strip_quotes, language_name, SOURCES, get_genera, population_info,
    get_rows, add_sources, feature_name,
)


def main(args):
    data = Data()
    unknown_genera = {}
    genera = get_genera(data)
    glottocodes, geocoords = {}, {}
    for k, v in glottocodes_by_isocode(
            'postgresql://robert@/glottolog3',
            cols=['id', 'latitude', 'longitude']).items():
        glottocodes[k] = v[0]
        geocoords[k] = (v[1], v[2])

    refs = defaultdict(list)
    for row in get_rows(args, 'BibtexKey'):
        if row[1] == 'NO SOURCE GIVEN':
            refs[row[0]] = []
        else:
            refs[row[0]].append(row[1])
    add_sources(args, data)

    dataset = data.add(
        common.Dataset, 'phoible',
        id='phoible',
        name='PHOIBLE Online',
        description='PHOIBLE Online',
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        domain='phoible.org',
        license='http://creativecommons.org/licenses/by-sa/3.0/',
        contact='steven.moran@uzh.ch',
        jsondata={
            'license_icon': 'http://i.creativecommons.org/l/by-sa/3.0/88x31.png',
            'license_name':
                'Creative Commons Attribution-ShareAlike 3.0 Unported License'})

    for i, spec in enumerate([
        ('moran', "Steven Moran"),
        ('mccloy', "Daniel McCloy"),
        ('wright', "Richard Wright"),
    ]):
        DBSession.add(common.Editor(
            dataset=dataset,
            ord=i + 1,
            contributor=common.Contributor(id=spec[0], name=spec[1])))

    squibs = defaultdict(list)
    for row in get_rows(args, 'Squib'):
        squibs[row[0]].append(row[1])

    source_urls = dict(get_rows(args, 'URL'))
    ia_urls = dict(get_rows(args, 'InternetArchive'))

    for row in reader(args.data_file('phoible-aggregated.tsv'), namedtuples=True):
        if row.InventoryID not in refs:
            print('--- skipping inventory', row.InventoryID)
            continue
        if row.LanguageCode not in data['Variety']:
            genus = slug(strip_quotes(row.LanguageFamilyGenus))
            if genus not in genera:
                print('-->', row.LanguageFamilyGenus)
                unknown_genera[genus] = 1
                genus = None
            else:
                genus = genera[genus]
                if genus and not genus.root:
                    genus.root = row.LanguageFamilyRoot
            population, population_comment = population_info(row.Population)
            coords = map(coord, [row.Latitude, row.Longitude])
            if coords[0] is None and row.LanguageCode in geocoords:
                coords = geocoords[row.LanguageCode]
            lang = data.add(
                models.Variety, row.LanguageCode,
                id=row.LanguageCode,
                name=language_name(row.LanguageName),
                genus=genus,
                country=strip_quotes(row.Country),
                area=strip_quotes(row.Area),
                population=population,
                population_comment=population_comment,
                latitude=coords[0],
                longitude=coords[1])
            add_language_codes(data, lang, lang.id, glottocodes=glottocodes)
        else:
            lang = data['Variety'][row.LanguageCode]

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
            models.Inventory, row.InventoryID,
            id=row.InventoryID,
            language=lang,
            source=source,
            source_url=source_urls.get(row.InventoryID),
            internetarchive_url=ia_urls.get(row.InventoryID),
            name='%s %s (%s)' % (row.InventoryID, lang.name, row.Source))

        DBSession.add(common.ContributionContributor(
            contribution=contrib, contributor=contributor))

        for j, squib in enumerate(squibs.get(row.InventoryID, [])):
            f = common.Contribution_files(
                object=contrib,
                id='squib-%s-%s.pdf' % (contrib.id, j + 1),
                name='Phonological squib',
                description=squib,
                mime_type='application/pdf')
            assert f
            # f.create(files_dir, file(args.data_file('phonological_squibs', src)).read())

    DBSession.flush()
    unknown_refs = {}

    for row in reader(args.data_file('phoible-phonemes.tsv'), namedtuples=True):
        if row.InventoryID not in refs:
            continue
        if row.LanguageCode == 'idn' and int(row.InventoryID) == 1690:
            lcode = 'ind'
        else:
            lcode = row.LanguageCode
        if lcode not in data['Variety']:
            print('skip phoneme with missing language code', row)
            continue
        if row.Phoneme not in data['Segment']:
            segment = data.add(
                models.Segment, row.Phoneme,
                id=row.GlyphID,
                name=row.Phoneme,
                description=' - '.join(unicodedata.name(c) for c in row.Phoneme),
                segment_class=row.Class,
                combined_class=row.CombinedClass)
            DBSession.flush()
        else:
            segment = data['Segment'][row.Phoneme]

        vs = common.ValueSet(
            id=row.PhonemeID,
            contribution=data['Inventory'][row.InventoryID],
            language=data['Variety'][lcode],
            parameter=segment)

        for ref in refs.get(row.InventoryID, []):
            if ref not in data['Source']:
                if ref not in unknown_refs:
                    print('-------', ref)
                unknown_refs[ref] = 1
                continue
            DBSession.add(common.ValueSetReference(
                source=data['Source'][ref],
                valueset=vs))

        DBSession.add(common.Value(
            id=row.PhonemeID,
            name='%s %s' % (row.Phoneme, data['Inventory'][row.InventoryID].name),
            valueset=vs))
        DBSession.flush()

    for inventory_id in refs:
        for ref in refs[inventory_id]:
            if ref not in data['Source']:
                continue
            data.add(
                common.ContributionReference, '%s-%s' % (inventory_id, ref),
                source=data['Source'][ref],
                contribution=data['Inventory'][inventory_id])

    for i, row in enumerate(reader(args.data_file('phoible-segments-features.tsv'))):
        if i == 0:
            features = list(map(feature_name, row))
            continue

        if row[0] not in data['Segment']:
            # print('skipping feature vector:', row)
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
    m = DBSession.query(models.Inventory).count()
    for segment in q:
        #
        # TODO: this ratio (number of inventories a segment appears in by number of
        # distinct segment total) doesn't make much sense, does it?
        #
        segment.frequency = float(len(segment.valuesets)) / float(n)
        segment.in_inventories = len(segment.valuesets)
        segment.total_inventories = m

    for inventory in DBSession.query(models.Inventory).options(
            joinedload_all(common.Contribution.valuesets, common.ValueSet.parameter)
    ):
        for vs in inventory.valuesets:
            attr = 'count_' + vs.parameter.segment_class
            if hasattr(inventory, attr):
                val = getattr(inventory, attr) or 0
                setattr(inventory, attr, val + 1)

    ficons = cycle(ORDERED_ICONS)
    gicons = cycle(ORDERED_ICONS)
    for root, genus in groupby(
            DBSession.query(models.Genus).order_by(models.Genus.description),
            lambda g: g.description):
        ficon = ficons.next().name
        for g in genus:
            g.ficon = ficon
            g.gicon = gicons.next().name

    for variety in DBSession.query(models.Variety).options(
            joinedload(models.Variety.inventories)):
        variety.count_inventories = len(variety.inventories)

    ia_func('update', args)
    gbs_func('update', args)


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
