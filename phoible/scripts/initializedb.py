from __future__ import unicode_literals, print_function
import sys
import unicodedata
from itertools import groupby, cycle
from collections import defaultdict
import socket
from base64 import b16encode
from hashlib import md5

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
    get_rows, add_sources, feature_name, add_wikipedia_urls,
)


astroman = socket.gethostname() == 'astroman'


def main(args):
    # determine if we run on a machine where other databases are available for lookup
    # locally:
    data = Data()
    genera = get_genera(data) if astroman else {}
    glottocodes, lnames, geocoords = {}, {}, {}
    if astroman:
        for k, v in glottocodes_by_isocode(
                'postgresql://robert@/glottolog3',
                cols=['id', 'name', 'latitude', 'longitude']).items():
            glottocodes[k] = v[0]
            lnames[k] = v[1]
            geocoords[k] = (v[2], v[3])

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

    aggregated = list(reader(args.data_file('phoible-aggregated.tsv'), namedtuples=True))
    inventory_names = {}
    for key, items in groupby(
            sorted(aggregated, key=lambda t: (t.LanguageCode, t.Source)),
            key=lambda t: (t.LanguageCode, t.Source)):
        items = list(items)

        lname = lnames.get(key[0])
        if not lname:
            lname = items[0].LanguageName
            lnames[key[0]] = lname

        if len(items) == 1:
            inventory_names[items[0].InventoryID] = '%s (%s)' % (lname, key[1])
        else:
            for i, item in enumerate(items):
                inventory_names[item.InventoryID] = '%s %s (%s)' % (lname, i + 1, key[1])

    for row in aggregated:
        lang = data['Variety'].get(row.LanguageCode)
        if not lang:
            if row.LanguageFamilyGenus == 'UNCLASSIFIED':
                genus = None
            else:
                genus_id = slug(strip_quotes(row.LanguageFamilyGenus))
                genus = genera.get(genus_id)
                if not genus:
                    genus = genera.get(row.LanguageCode)
                    if not genus:
                        genus = genera[genus_id] = data.add(
                            models.Genus, genus_id,
                            id=genus_id,
                            name=row.LanguageFamilyGenus,
                            description=row.LanguageFamilyRoot,
                            active=False,
                            root=row.LanguageFamilyRoot)

                if not genus.root:
                    genus.root = row.LanguageFamilyRoot

            population, population_comment = population_info(row.Population)
            if row.LanguageCode in geocoords:
                coords = geocoords[row.LanguageCode]
            elif row.Latitude != 'NULL' and row.Longitude != 'NULL':
                coords = (float(row.Latitude), float(row.Longitude))
            lang = data.add(
                models.Variety, row.LanguageCode,
                id=row.LanguageCode,
                name=lnames[row.LanguageCode],
                genus=genus,
                country=strip_quotes(row.Country),
                area=strip_quotes(row.Area),
                population=population,
                population_comment=population_comment,
                latitude=coords[0],
                longitude=coords[1],
                jsondata=dict(inventory_id=row.InventoryID))
            add_language_codes(data, lang, row.LanguageCode, glottocodes=glottocodes)

        contributor = data['Contributor'].get(row.Source)
        if not contributor:
            contributor = data.add(
                common.Contributor, row.Source,
                id=row.Source,
                name=SOURCES[row.Source][0],
                description=SOURCES[row.Source][2])
            for ref in SOURCES[row.Source][1]:
                DBSession.add(models.ContributorReference(
                    source=data['Source'][ref], contributor=contributor))

        contrib = data.add(
            models.Inventory, row.InventoryID,
            id=row.InventoryID,
            language=lang,
            source=row.Source,
            source_url=source_urls.get(row.InventoryID),
            internetarchive_url=ia_urls.get(row.InventoryID),
            name=inventory_names[row.InventoryID],
            description=row.LanguageName)

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
        inventory = data['Inventory'][row.InventoryID]
        segment = data['Segment'].get(row.Phoneme)
        if not segment:
            unicode_desc = [(c, unicodedata.name(c)) for c in row.Phoneme]
            description = ' - '.join([t[1] for t in unicode_desc])
            segment = data.add(
                models.Segment, row.Phoneme,
                id=b16encode(md5(description).digest()),
                name=row.Phoneme,
                description=description,
                equivalence_class=''.join(
                    [t[0] for t in unicode_desc
                     if t[1].split()[0] not in ['COMBINING', 'MODIFIER']]),
                segment_class=row.Class,
                combined_class=row.CombinedClass)
            DBSession.flush()

        vs = common.ValueSet(
            id=row.PhonemeID,
            contribution=inventory,
            language=inventory.language,
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
        if '(UPSID)' not in inventory.name:
            inventory.count_tone = 0

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

    if astroman:
        ia_func('update', args)
        gbs_func('update', args)
        print('added', add_wikipedia_urls(args), 'wikipedia urls')


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
