from clld.web.assets import environment
from clldutils.path import Path

import phoible


environment.append_path(
    Path(phoible.__file__).parent.joinpath('static').as_posix(), url='/phoible:static/')
environment.load_path = list(reversed(environment.load_path))
