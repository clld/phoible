# coding: utf8
from __future__ import unicode_literals


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
    s = strip_quotes(s.split(';')[0])
    for sep in ['-', ' ', '(']:
        if sep in s:
            s = sep.join(ss.capitalize() for ss in s.split(sep))
    return s.capitalize()
