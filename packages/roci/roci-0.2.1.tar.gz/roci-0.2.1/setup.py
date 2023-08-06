# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['roci', 'roci.structure.src', 'roci.structure.tests']

package_data = \
{'': ['*'],
 'roci': ['structure/.github/workflows/*',
          'structure/.gitignore',
          'structure/.gitignore',
          'structure/.gitignore',
          'structure/.gitignore',
          'structure/Makefile',
          'structure/Makefile',
          'structure/Makefile',
          'structure/Makefile',
          'structure/README.md',
          'structure/README.md',
          'structure/README.md',
          'structure/README.md',
          'structure/docs/*',
          'structure/requirements.txt',
          'structure/requirements.txt',
          'structure/requirements.txt',
          'structure/requirements.txt'],
 'roci.structure.src': ['data/*']}

entry_points = \
{'console_scripts': ['roci = roci:direc_dumper']}

setup_kwargs = {
    'name': 'roci',
    'version': '0.2.1',
    'description': 'no longer a work horse',
    'long_description': '# Roci\n\n![pypi](https://img.shields.io/pypi/v/roci.svg)](https://pypi.org/project/roci/)\n![Linting](https://github.com/andrewblance/roci/workflows/Linting/badge.svg)\n',
    'author': 'Andrew Blance',
    'author_email': 'andrewblance@live.co.uk',
    'url': 'https://github.com/andrewblance/roci',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
