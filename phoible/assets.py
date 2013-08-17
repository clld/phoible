from clld.web.assets import environment
from path import path

import phoible


environment.append_path(
    path(phoible.__file__).dirname().joinpath('static'), url='/phoible:static/')
environment.load_path = list(reversed(environment.load_path))
