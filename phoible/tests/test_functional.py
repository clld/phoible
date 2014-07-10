# coding: utf8
from path import path

from clld.tests.util import TestWithApp

import phoible


class Tests(TestWithApp):
    __cfg__ = path(phoible.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get('/')
        self.app.get('/void.md.txt')

    def test_segments(self):
        self.app.get_dt('/parameters')
        self.app.get_dt('/parameters?sSearch_1=>100&iSortingCols=1&iSortCol_0=1')
        self.app.get_html('/parameters')
        self.app.get_html('/parameters/1')
        self.app.get_xml('/parameters/1.rdf')
        self.app.get_json('/parameters/1.geojson')

    def test_inventories(self):
        self.app.get_dt('/inventories')
        self.app.get_dt('/inventories?sSearch_1=>20&iSortingCols=1&iSortCol_0=1')
        self.app.get_dt('/inventories?sSearch_5=a&iSortingCols=1&iSortCol_0=5')
        self.app.get_html('/inventories')
        self.app.get_html('/inventories/view/432')
        self.app.get_xml('/inventories/view/432.rdf')
        self.app.get('/inventories/view/432.md.ris')
        self.app.get('/inventories/view/432.md.bib')
        self.app.get('/inventories/view/432.md.html')

    def test_languages(self):
        self.app.get_dt('/languages')
        self.app.get_dt('/languages?sSearch_2=a&iSortingCols=1&iSortCol_0=2')
        self.app.get_dt('/languages?sSearch_3=a&iSortingCols=1&iSortCol_0=3')
        self.app.get('/languages')
        self.app.get_json('/languages.geojson')
        self.app.get('/languages/ktz')
        self.app.get_xml('/languages/ktz.rdf')

    def test_phonemes(self):
        self.app.get_dt('/values?parameter=1')
        self.app.get_dt('/values?parameter=1&sSearch_0=a&iSortingCols=1&iSortCol_0=0')
        self.app.get_dt(
            '/values?contribution=1003&sSearch_0=a&iSortingCols=1&iSortCol_0=0')

    def test_sources(self):
        self.app.get_html('/sources/saphon')
