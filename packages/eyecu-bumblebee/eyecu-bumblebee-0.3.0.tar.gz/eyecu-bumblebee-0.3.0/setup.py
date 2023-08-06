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
    'version': '0.3.0',
    'description': 'Advanced pipelines for video datasets',
    'long_description': '# Bumblebee\n\n![Bumblebee image](./docs/bumblebee.png)\n\n\n## Architecture Diagram\n\n![Architecture](docs/bumblebee_arch_diagram.png)\n\n\n## Example Pipeline\n\n```python\nfrom bumblebee import *\n\nif __name__ == "__main__":\n\n    VIDEO_PATH = "/path/to/video.mp4" # Path to video\n    \n    # Create a source\n    file_stream = sources.FileStream(VIDEO_PATH)\n    \n    # Add goto effect\n    goto        = effects.GoTo(file_stream)\n    \n    # Add some transformers\n    data        = transfomers.GrayScale(file_stream)\n    data        = transfomers.Normalization(data)\n\n    \n    END_OF_VIDEO = file_stream.get_duration()\n    # Goto end of video\n    goto(END_OF_VIDEO) \n    \n    # Create a dataset\n    dataset = datasets.SingleFrame(data)\n    \n    # Last frame of video\n    last_frame = dataset.read()\n\n```',
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
