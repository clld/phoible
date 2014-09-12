# coding: utf8
from __future__ import unicode_literals
from itertools import chain
from io import open

from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine
from clld.util import slug, nfilter
from clld.lib.dsv import reader
from clld.lib.bibtex import Database, Record
from clld.scripts.util import bibtex2source
from clld.db.meta import DBSession
from clld.db.models.common import Source, Parameter

from phoible import models


SOURCES = {
    'AA': (
        'Christian Chanard and Rhonda L. Hartell',
        ['Hartell1993', 'Chanard2006'],
        'The inventories in Alphabets of Africa (AA) come from the work of Christian '
        'Chanard\'s <a href="http://sumale.vjf.cnrs.fr/phono/">Syst&egrave;mes '
        'alphab&eacute;tiques des langues africaines</a>, an online database of the work '
        'of <em>Alphabets des langues africaines</em>, published in 1993 by the Regional '
        'Office in Dakar, Senegal, and edited by Rhonda L. Hartell. AA contains the '
        'phoneme inventories and orthographies of 200 languages. Incorrect ISO 639-3 '
        'language name identifiers and incorrect Unicode IPA characters were updated '
        'before the inventories from the online version were added to PHOIBLE (see '
        'Moran 2012, chp 4 for details). Christopher Green verified the inventories\' '
        'contents and in cases where there were discrepencies between Chanard and '
        'Hartell, additional resources were consulted to resolve these issues (ibid.).',
    ),
    'PH': (
        'PHOIBLE',
        ['Moran2012a'],
        'Steven Moran and Daniel McCloy and Richard Wright.',
        'PHOIBLE inventories were extracted from secondary resources including grammars '
        'and phonological descriptions by members of the Phonetics Lab and the University'
        ' of Washington (see credits page and Moran 2012, chp 4). Inventories include '
        'descriptions of phonemes, allophones and their conditioning environments, '
        'although in the current version of PHOIBLE Online only phoneme inventories are '
        'available.'
    ),
    'SPA': (
        'Stanford Phonology Archive',
        ['SPA1979'],
        "The Stanford Phonology Archive (SPA) was the first computerized database of "
        "phonological segment inventories. It was inspired by Joseph Greenberg's "
        "research on universals and his personal archive of data from notebooks and his "
        "memory (Crothers et al 1979, i-ii). The inventories in PHOIBLE Online come from "
        "the <em>Handbook of Phonological Data From a Sample of the World's "
        "Languages</em>, compiled and edited by Crothers et al 1979, and kindly provided "
        "to the Phonetics Lab (University of Washington) by Marilyn M. Vihman. The "
        "inventories in SPA include descriptions of phonemes, allophones and comments "
        "on phonological contexts for 197 languages. The inventory descriptions were "
        "digitized and each phoneme was mapped from its original written description, "
        "e.g. d-pharyngealized, to a Unicode IPA representation. Each inventory was also "
        "assigned an ISO 639-3 language name identifer. Details are given in Moran 2012, "
        "chp 4, and the SPA-to-Unicode IPA mappings are given in Moran 2012, appendix E."
    ),
    'GM': (
        'Christopher Green and Steven Moran',
        [],
        'Christopher Green and Steven Moran extracted phonological inventories from '
        'secondary sources including grammars and phonological descriptions with the '
        'goal of attaining pan-Africa coverage. This is a work in progress.'),
    'RA': (
        'Ramaswami, N.',
        ['ramaswami1999'],
        "These inventories come from <em>Common Linguistic Features in Indian Languages: "
        "Phoentics</em>, by N. Ramaswami. This source contains 100 languages' phoneme "
        "inventories, as compiled from various works on languages of India."),
    'SAPHON': (
        'South American Phonological Inventory Database',
        ['saphon'],
        'The South American Phonological Inventory Database (SAPHON), compiled and '
        'edited by Lev Michael, Tammy Stark and Will Chang, is a comprehensive resource '
        'describing phoneme inventories from languages spoken in South America. It '
        'contains over 300 data points and is available online at: '
        '<a href="http://linguistics.berkeley.edu/~saphon/">'
        'http://linguistics.berkeley.edu/~saphon/</a>.'),
    'UPSID': (
        'UCLA Phonological Segment Inventory Database',
        ['Maddieson1984', 'MaddiesonPrecoda1990'],
        "In the early 1980's, Ian Maddieson developed the UCLA Phonological Segment "
        "Inventory Database (UPSID), a computer-accessible database of contrastive "
        "segment inventories (Maddieson 1984). The initial sample of 317 languages drew "
        "on the work of the Stanford Phonology Archive (Crothers et al 1979), but "
        "decisions regarding the phonemic status and phonetic descriptions of some "
        "segments do not coincide between the compilers of the two databases and were "
        "therefore updated in UPSID (Maddieson 1984, pg 6). Maddieson and Precoda (1990) "
        "expanded the sample of languages from 317 to 451; both datasets have been based "
        "on a quota sampling technique that aims to include one language from each small "
        "language family. UPSID inventories contain no descriptions of tone. The "
        "UPSID-451 data used in PHOIBLE Online were extracted from a DOS software "
        "package. Each segment description, originally given in an ASCII encoding "
        "(e.g. XW9:) was mapped to Unicode IPA and each inventory was assigned an "
        "ISO 639-3 language name identifier. For details, see Moran 2012, chp 4; the "
        "UPSID-to-Unicode mappings are given in Moran 2012, appendix F.")}

BIB = """\
@book{ramaswami1999,
        Author = {Ramaswami, N.},
        Title = {Common Linguistic Features in Indian Languages: Phonetics},
        Publisher = {Central	Institute of Indian Languages},
        Place = {Mysore, India},
        Year = {1999}
}

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
@techreport{IPA2005,
        Author = {{International {P}honetic {A}ssociation}},
        Institution = {International Phonetic Association},
        Title = {{International Phonetic Alphabet}},
        Url = {http://www.arts.gla.ac.uk/IPA/},
        Year = {2005}
}
@article{Cysouw_etal2012,
    Author = {Michael Cysouw and Dan Dediu and Steven Moran},
    Journal = {Science},
    Pages = {657--b},
    Publisher = {Science},
    Title = {{Still No Evidence for an Ancient Language Expansion From Africa}},
    Url = {http://www.sciencemag.org/content/335/6069/657.2.full},
    Volume = {335},
    Year = {2012}}

@misc{mccloy_etal2013,
    author = {{McCloy}, Daniel R. and Moran, Steven and Wright, Richard A.},
    title = {Revisiting `The role of features in phonological inventories'},
    year = {2013},
    month = jan,
    howpublished = {CUNY Conference on the Feature in Phonology and Phonetics},
    address = {New York, {NY}},
    type = {paper},
    url = {http://students.washington.edu/drmccloy/pubs/McCloyEtAl2013_cunyFeatureConf.pdf},
}
@incollection{Moran2012b,
    Address = {Heidelberg},
    Author = {Moran, Steven},
    Booktitle = {Linked Data in Linguistics: Representing and Connecting Language Data and Language Metadata},
    Editor = {Chiarcos, Christian and Nordhoff, Sebastian and Hellmann, Sebastian},
    Isbn = {978-3-642-28249-2},
    Note = {doi:10.1007/978-3-642-28249-2\_13},
    Pages = {129--138},
    Publisher = {Springer},
    Title = {{Using Linked Data to Create a Typological Knowledge Base}},
    Url = {http://www.springer.com/computer/ai/book/978-3-642-28248-5},
    Year = {2012}}

@article{Moran_etal2012,
    Author = {Steven Moran and Daniel McCloy and Richard Wright},
    Journal = {Language},
    Number = {4},
    Pages = {877--893},
    Title = {{Revisiting Population Size vs. Phoneme Inventory Size}},
    Volume = {88},
    Url = {http://dx.doi.org/10.1353/lan.2012.0087},
    Year = {2012}}

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


def capitalize(s):
    if not s:
        return s

    if s.lower() in ['dialect)', 'dialects)', 'and', 'do', 'del', 'de']:
        return s.lower()

    return s[0].upper() + s[1:]


def language_name(s):
    """normalize a language name
    """
    s = strip_quotes(s.split(';')[0])
    for sep in ['-', '(', ' ']:
        if sep in s:
            s = sep.join(capitalize(ss) for ss in s.split(sep))
    if s[0].islower() or (len(s) > 1 and s[1].isupper()):
        # only capitalize if not done already - or if it's all uppercase.
        if len(s) > 1 and s[1].isupper():
            s = s.capitalize()
        else:
            s = capitalize(s)
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
    """
    Zo'e: tupiguarani
    """
    sql = """select g.id, g.name, f.name
from genus as g, family as f
where g.family_pk = f.pk"""
    walsdb = create_engine('postgresql://robert@/wals3')
    genera = {}
    for row in walsdb.execute(sql):
        genus = data.add(models.Genus, row[0], id=row[0], name=row[1], description=row[2])
        genera[row[0]] = genus
        genera[slug(row[1])] = genus

    sql = """select l.iso_codes, g.id
from walslanguage as l, genus as g
where l.genus_pk = g.pk and l.iso_codes is not null"""
    for row in walsdb.execute(sql):
        for code in row[0].split(', '):
            if code not in genera:
                genera[code] = genera[row[1]]

    for row in walsdb.execute("select key, value from config"):
        if row[0].startswith('__Genus_'):
            gid = row[0].replace('_', '').split('Genus', 1)[1]
            genera[gid] = None if row[1] == '__gone__' else genera[row[1]]
    return genera


def get_rows(args, name):
    for i, row in enumerate(reader(args.data_file('InventoryID-%s.csv' % name))):
        if i and row[1] != 'NA':
            yield row


def add_wikipedia_urls(args):
    links = {}
    with open(
            args.data_file('International_Phonetic_Alphabet.htm'), encoding='utf8') as fp:
        for a in bs(fp.read()).find_all('a', href=True):
            links[a.text] = a['href']

    count = 0
    for p in DBSession.query(Parameter):
        if p.name in links:
            p.update_jsondata(wikipedia_url='http://en.wikipedia.org' + links[p.name])
            count += 1
        elif p.equivalence_class in links:
            p.update_jsondata(
                wikipedia_url='http://en.wikipedia.org' + links[p.equivalence_class])
            count += 1

    return count
