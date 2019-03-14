import sys
from collections import defaultdict
import unicodedata

from sqlalchemy.orm import joinedload, joinedload_all
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import color

from clld.lib.bibtex import EntryType, FIELDS, unescape, Record
from pyglottolog.api import Glottolog
from clld_glottologfamily_plugin.util import load_families
from pycldf import StructureDataset
from nameparser import HumanName
from clldutils.path import Path
from clldutils.misc import nfilter
from clldutils.jsonlib import load

import phoible
from phoible import models
from phoible.scripts.util import get_rows, add_wikipedia_urls, BIB, feature_name


DS = Path(phoible.__file__).parent.parent.parent / 'phoible-cldf' / 'cldf' / 'StructureDataset-metadata.json'


def bibtex2source(rec):  # pragma: no cover
    year = rec.get('year', 'nd')
    fields = {}
    jsondata = {}
    for field in FIELDS:
        if field in rec:
            value = unescape(rec[field])
            container = fields if hasattr(common.Source, field) else jsondata
            container[field] = value
            # remove \\ from url fields!
            if field == 'url':
                container[field] = container[field].replace('\\', '')

    etal = ''
    eds = ''
    authors = rec.get('author')
    if not authors:
        authors = rec.get('editor', '')
        if authors:
            eds = ' (eds.)'
    if authors:
        authors = unescape(authors).split(' and ')
        if len(authors) > 2:
            authors = authors[:1]
            etal = ' et al.'

        authors = [HumanName(a) for a in authors]
        authors = [n.last or n.first for n in authors]
        authors = '%s%s%s' % (' and '.join(authors), etal, eds)

    if rec.genre == 'thesis':
        if rec['type'] == 'phdthesis':
            rec.genre = 'phdthesis'
        else:
            rec.genre = 'mastersthesis'

    try:
        bibtex_type = EntryType.from_string(rec.genre)
    except:
        bibtex_type = EntryType.from_string('misc')

    return common.Source(
        id=rec.id,
        name=('%s %s' % (authors, year)).strip(),
        description=unescape(rec.get('title', rec.get('booktitle', ''))),
        jsondata=jsondata,
        bibtex_type=bibtex_type,
        **fields)


def main(args):  # pragma: no cover
    ds = StructureDataset.from_metadata(DS)
    data = Data()
    for source in ds.sources:
        data.add(common.Source, source.id, _obj=bibtex2source(source))

    ext = [Record.from_string('@' + s, lowercase=True) for s in nfilter(BIB.split('@'))]
    for rec in ext:
        if rec.id not in data['Source']:
            data.add(common.Source, rec.id, _obj=bibtex2source(rec))


    for contrib in ds['contributors.csv']:
        o = data.add(
            common.Contributor,
            contrib['ID'],
            id=contrib['ID'].upper(),
            name=contrib['Name'],
            description=contrib['Description'],
            url=contrib['URL'],
            jsondata={'readme': contrib['Readme'], 'contents': contrib['Contents']},
        )
        for src in contrib['Source']:
            DBSession.add(models.ContributorReference(source=data['Source'][src], contributor=o))

    dataset = data.add(
        common.Dataset, 'phoible',
        id='phoible',
        name='PHOIBLE 2.0',
        description='PHOIBLE 2.0',
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="https://www.shh.mpg.de",
        domain='phoible.org',
        license='https://creativecommons.org/licenses/by-sa/3.0/',
        contact='steven.moran@uzh.ch',
        jsondata={
            'license_icon': 'https://i.creativecommons.org/l/by-sa/3.0/88x31.png',
            'license_name':
                'Creative Commons Attribution-ShareAlike 3.0 Unported License'})

    for i, (cid, name) in enumerate([
        ('UZ', "Steven Moran"),
        ('mccloy', "Daniel McCloy"),
    ], start=1):
        contrib = data['Contributor'].get(cid)
        if not contrib:
            contrib = common.Contributor(id=cid, name=name)
        DBSession.add(common.Editor(dataset=dataset, ord=i, contributor=contrib))

    glottolog = Glottolog(
        Path(phoible.__file__).parent.parent.parent.parent.joinpath(
            'glottolog', 'glottolog'))

    for lang in ds['LanguageTable']:
        l = data.add(
            models.Variety,
            lang['ID'],
            id=lang['ID'],
            name=lang['Name'],
        )

    load_families(
        data, [(l.id, l) for l in data['Variety'].values() if len(l.id) == 8], glottolog.repos)
    DBSession.flush()

    # assign color codes:
    families = defaultdict(list)
    for l in data['Variety'].values():
        families[l.family_pk].append(l)

    colors = color.qualitative_colors(len(families))
    for i, langs in enumerate(sorted(families.values(), key=lambda v: -len(v))):
        for l in langs:
            l.jsondata = {'color': colors[i]}

    for segment in ds['ParameterTable']:
        equivalence_class = ''.join([
            t[0] for t in [(c, unicodedata.name(c)) for c in segment['Name']]
            if t[1].split()[0] not in ['COMBINING', 'MODIFIER']]),
        data.add(
            models.Segment,
            segment['ID'],
            id=segment['ID'],
            name=segment['Name'],
            description=segment['Description'],
            segment_class=segment['SegmentClass'],
            equivalence_class=equivalence_class
        )
    DBSession.flush()
    for segment in ds['ParameterTable']:
        for i, (k, v) in enumerate(sorted(segment.items())):
            if k not in ['ID', 'Name', 'Description', 'SegmentClass']:
                DBSession.add(common.Parameter_data(
                    key=feature_name(k),
                    value=v,
                    ord=i,
                    object_pk=data['Segment'][segment['ID']].pk))

    for inventory in ds['contributions.csv']:
        inv = data.add(
            models.Inventory,
            inventory['ID'],
            id=inventory['ID'],
            name='{0} ({1} {2})'.format(
                inventory['Name'],
                inventory['Contributor_ID'].upper(),
                inventory['ID'],
            ),
            source_url=inventory['URL'],
        )
        DBSession.add(common.ContributionContributor(contribution=inv, contributor=data['Contributor'][inventory['Contributor_ID'].upper()]))
        for src in inventory['Source']:
            DBSession.add(common.ContributionReference(contribution=inv, source=data['Source'][src]))

    for phoneme in ds['ValueTable']:
        lang = data['Variety'][phoneme['Language_ID']]
        inv = data['Inventory'][phoneme['Contribution_ID']]
        if not inv.language:
            inv.language = lang
        vs = common.ValueSet(
            id=phoneme['ID'],
            contribution=inv,
            language=lang,
            parameter=data['Segment'][phoneme['Parameter_ID']])

        for ref in phoneme['Source']:
            DBSession.add(common.ValueSetReference(source=data['Source'][ref], valueset=vs))

        DBSession.add(models.Phoneme(
            id=phoneme['ID'],
            name='%s %s' % (phoneme['Value'], data['Inventory'][phoneme['Contribution_ID']].name),
            allophones=' '.join(phoneme['Allophones']),
            marginal=phoneme['Marginal'],
            valueset=vs))

    # Add redirects for old language pages! get relevant ISO codes and map to Glottocode!
    for model, repls in load(Path(phoible.__file__).parent.parent / 'replacements.json').items():
        if model == 'Language':
            languoids = {l.iso: l.id for l in glottolog.languoids() if l.iso}
            for oid, nid in repls.items():
                common.Config.add_replacement(oid, languoids.get(oid), common.Language)
        elif model == 'Parameter':
            for oid, nid in repls.items():
                common.Config.add_replacement(oid, nid, common.Parameter)
    return

    ia_urls = dict(get_rows(args, 'InternetArchive'))

    #squibs = defaultdict(list)
    #for row in get_rows(args, 'Squib'):
    #    squibs[row[0]].append(row[1])



    #for row in aggregated:
        #for j, squib in enumerate(squibs.get(row.InventoryID, [])):
        #    f = common.Contribution_files(
        #        object=contrib,
        #        id='squib-%s-%s.pdf' % (contrib.id, j + 1),
        #        name='Phonological squib',
        #        description=squib,
        #        mime_type='application/pdf')
        #    assert f
        #    # f.create(files_dir, file(args.data_file('phonological_squibs', src)).read())



def prime_cache(args):  # pragma: no cover
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

    for variety in DBSession.query(models.Variety).options(
            joinedload(models.Variety.inventories)):
        variety.count_inventories = len(variety.inventories)

    print('added', add_wikipedia_urls(), 'wikipedia urls')


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
