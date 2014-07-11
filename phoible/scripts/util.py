# coding: utf8
from __future__ import unicode_literals
from itertools import chain

from sqlalchemy import create_engine
from clld.util import slug, nfilter
from clld.lib.dsv import reader
from clld.lib.bibtex import Database, Record
from clld.scripts.util import bibtex2source
from clld.db.models.common import Source

from phoible import models


SOURCES = {
    'AA': (
        'C. Chanard and Rhonda L. Hartell',
        ['Hartell1993', 'Chanard2006'],
        'Chanard and Hartell'),
    'UW': (
        'PHOIBLE',
        ['Moran2012a'],
        'Steven Moran and Daniel McCloy and Richard Wright'),
    'SPA': (
        'Stanford Phonology Archive',
        ['SPA1979'],
        'John H. Crothers et al.'),
    'CASL': (
        'Center for Advanced Study of Language',
        [],
        'Chris Green and Steven Moran'),
    'Ramaswami': (
        'Ramaswami, N.',
        ['ramaswami1982'],
        'N. Ramaswami'),
    'SAPHON': (
        'South American Phonological Inventory Database',
        ['saphon'],
        'Lev Michael and Tammy Stark and Will Chang'),
    'UPSID': (
        'UCLA Phonological Segment Inventory Database',
        ['Maddieson1984', 'MaddiesonPrecoda1990'],
        'Ian Maddieson and Kristin Precoda')}

BIB = """\
@misc{ramaswami1982,
        Author = {Ramaswami, N.},
        Title = {{Brokskat}},
        Year = {1982}
}
@misc{saphon,
        Author = {Michael, Lev, Tammy Stark, and Will Chang},
        Url = {http://linguistics.berkeley.edu/~saphon/en/},
        Title = {{South American Phonological Inventory Database}},
        Place = {Berkeley},
        Publisher = {University of California},
        Year = {2012}
}
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
        booktitle={Proceedings of the International Congress of Phonetic Sciences \
(ICPhS XVII)},
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
        Author = {John H. Crothers and James P. Lorentz and Donald A. Sherman and \
Marilyn M. Vihman},
        Title = {Handbook of Phonological Data From a Sample of the World's Languages: \
A Report of the Stanford Phonology Archive},
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


def add_sources(args, data):
    bib = Database.from_file(args.data_file('phoible-references.bib'), lowercase=True)
    ext = [Record.from_string('@' + s, lowercase=True) for s in nfilter(BIB.split('@'))]

    for rec in chain(ext, bib):
        if rec.id not in data['Source']:
            data.add(Source, rec.id, _obj=bibtex2source(rec))

    #
    # add aliases to lookup records with bibtex keys with numeric prefixes without
    # specifying the prefix
    #
    for key in list(data['Source'].keys()):
        if '_' in key:
            no, rem = key.split('_', 1)
            try:
                int(no)
                if rem not in data['Source']:
                    data['Source'][rem] = data['Source'][key]
            except (ValueError, TypeError):
                pass


def coord(s):
    if s.endswith('-00'):
        s = s[:-3]

    if ':' not in s:
        return
    s = s.replace('`N', '')
    deg, min_ = s.split(':')

    def strip_leading_zeros(ss):
        while ss.startswith('0'):
            ss = ss[1:]
        return ss

    try:
        return float(strip_leading_zeros(deg) or 0) + \
            float(strip_leading_zeros(min_) or 0) / 60.0
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
    """normalize a language name
    """
    s = strip_quotes(s.split(';')[0])
    for sep in ['-', ' ', '(', ',', "'"]:
        if sep in s:
            s = sep.join(ss.capitalize() for ss in s.split(sep))
    if s[0].islower() or (len(s) > 1 and s[1].isupper()):
        # only capitalize if not done already - or if it's all uppercase.
        s = s.capitalize()
    return s


def feature_name(n):
    """normalize a feature name as encountered as column header in features.tsv

    converts camel case into space separated lowercase words.
    """
    chars = []
    for char in n:
        if char.isupper():
            chars.append(' ' + char.lower())
        else:
            chars.append(char)
    return ''.join(chars)


def get_genera(data):
    sql = """select g.id, g.name, f.name
from genus as g, family as f
where g.family_pk = f.pk"""
    walsdb = create_engine('postgresql://robert@/wals3')
    genera = {'unclassified': None}
    for row in walsdb.execute(sql):
        genus = data.add(models.Genus, row[0], id=row[0], name=row[1], description=row[2])
        genera[row[0]] = genus
        genera[slug(row[1])] = genus

    for row in walsdb.execute("select key, value from config"):
        if row[0].startswith('__Genus_'):
            gid = row[0].replace('_', '').split('Genus', 1)[1]
            genera[gid] = None if row[1] == '__gone__' else genera[row[1]]
    return genera


def population_info(s):
    if s in ['Missing E16 page']:
        return 0, ''
    if s in ['Extinct', 'No_known_speakers', 'No_estimate_available', 'Ancient']:
        return 0, s.replace('_', ' ').lower()
    return int(s.replace(',', '')), ''


def get_rows(args, name):
    for i, row in enumerate(reader(args.data_file('InventoryID-%s.csv' % name))):
        if i and row[1] != 'NA':
            yield row
