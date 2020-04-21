import pathlib

from clld.web.assets import environment

import phoible


environment.append_path(
    str(pathlib.Path(phoible.__file__).parent.joinpath('static')), url='/phoible:static/')
environment.load_path = list(reversed(environment.load_path))
