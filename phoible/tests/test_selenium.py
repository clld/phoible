from clld.tests.util import TestWithSelenium

import phoible


class Tests(TestWithSelenium):
    app = phoible.main({}, **{'sqlalchemy.url': 'postgres://robert@/phoible'})
