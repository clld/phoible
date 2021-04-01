import requests
from bs4 import BeautifulSoup as bs
from csvw.dsv import reader
from clld.db.meta import DBSession
from clld.db.models.common import Parameter


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
        Url = {https://digital.lib.washington.edu/researchworks/handle/1773/22452},
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
    month = {Jan},
    howpublished = {CUNY Conference on the Feature in Phonology and Phonetics},
    address = {New York, {NY}},
    type = {paper},
    url = {https://dan.mccloy.info/pubs/McCloyEtAl2013_cunyFeatureConf.pdf}
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


def feature_name(n):  # pragma: no cover
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


def get_rows(args, name):  # pragma: no cover
    for i, row in enumerate(
            reader(args.data_file('InventoryID-%s.csv' % name), delimiter='\t')):
        if i and row[1] != 'NA':
            yield row


def add_wikipedia_urls():  # pragma: no cover
    links = {}
    for a in bs(requests.get('https://en.wikipedia.org/wiki/International_Phonetic_Alphabet').text).find_all('a', href=True):
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
