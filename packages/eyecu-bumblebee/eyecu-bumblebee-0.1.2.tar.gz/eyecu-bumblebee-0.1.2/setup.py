# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eyecu_bumblebee',
 'eyecu_bumblebee.image',
 'eyecu_bumblebee.video',
 'eyecu_bumblebee.video.datasets',
 'eyecu_bumblebee.video.enhancers',
 'eyecu_bumblebee.video.interfaces',
 'eyecu_bumblebee.video.streams',
 'eyecu_bumblebee.video.transfomers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eyecu-bumblebee',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
