# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eyecu_bumblebee',
 'eyecu_bumblebee.video',
 'eyecu_bumblebee.video.datasets',
 'eyecu_bumblebee.video.effects',
 'eyecu_bumblebee.video.interfaces',
 'eyecu_bumblebee.video.sources',
 'eyecu_bumblebee.video.transfomers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eyecu-bumblebee',
    'version': '0.2.0',
    'description': 'Advanced training methods on videos.',
    'long_description': None,
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
