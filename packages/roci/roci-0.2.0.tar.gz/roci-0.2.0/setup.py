# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['roci', 'roci.structure.src', 'roci.structure.tests']

package_data = \
{'': ['*'],
 'roci': ['structure/*', 'structure/.github/workflows/*', 'structure/docs/*'],
 'roci.structure.src': ['data/*'],
 'roci.structure.tests': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

entry_points = \
{'console_scripts': ['roci = roci:direc_dumper']}

setup_kwargs = {
    'name': 'roci',
    'version': '0.2.0',
    'description': 'no longer a work horse',
    'long_description': None,
    'author': 'Andrew Blance',
    'author_email': 'andrewblance@live.co.uk',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
