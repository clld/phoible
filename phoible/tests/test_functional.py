from path import path

from clld.tests.util import TestWithApp

import phoible


class Tests(TestWithApp):
    __cfg__ = path(phoible.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        res = self.app.get('/', status=200)

    def test_inventories(self):
        res = self.app.get('/inventories', status=200)
        res = self.app.get('/inventories/view/1', status=200)

    def test_parameter(self):
        res = self.app.get('/parameters/1.geojson')

    def test_source(self):
        res = self.app.get('/sources/yuc_linn2001')
