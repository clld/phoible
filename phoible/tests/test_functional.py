# coding: utf8
from path import path

from clld.tests.util import TestWithApp

import phoible


class Tests(TestWithApp):
    __cfg__ = path(phoible.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get('/', status=200)

    def test_segments(self):
        self.app.get('/parameters?sEcho=1', xhr=True, status=200)
        self.app.get('/parameters', status=200)
        self.app.get('/parameters/1', status=200)

    def test_inventories(self):
        self.app.get('/inventories?sEcho=1', xhr=True, status=200)
        self.app.get('/inventories', status=200)
        self.app.get('/inventories/view/432', status=200)

    def test_languages(self):
        self.app.get('/languages?sEcho=1', xhr=True, status=200)
        self.app.get('/languages', status=200)
        self.app.get('/languages/ktz', status=200)

    def test_phonemes(self):
        self.app.get('/values?sEcho=1&parameter=1', xhr=True, status=200)
