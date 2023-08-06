# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bumblebee',
 'bumblebee.datasets',
 'bumblebee.effects',
 'bumblebee.interfaces',
 'bumblebee.sources',
 'bumblebee.transfomers']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hi = hello:hello']}

setup_kwargs = {
    'name': 'eyecu-bumblebee',
    'version': '0.2.3',
    'description': 'Advanced pipelines for video datasets',
    'long_description': '# Bumblebee\n\n![Bumblebee image](./docs/bumblebee.png)\n\n\n## Architecture Diagram\n\n![Architecture](docs/bumblebee_arch_diagram.png)\n',
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Eye-C-U/bumblebee/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
