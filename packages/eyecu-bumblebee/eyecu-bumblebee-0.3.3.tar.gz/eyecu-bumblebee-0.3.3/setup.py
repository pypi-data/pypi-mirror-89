# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bumblebee',
 'bumblebee.datasets',
 'bumblebee.effects',
 'bumblebee.interfaces',
 'bumblebee.sources',
 'bumblebee.transformers']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'opencv-python>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['hi = hello:hello']}

setup_kwargs = {
    'name': 'eyecu-bumblebee',
    'version': '0.3.3',
    'description': 'Advanced pipelines for video datasets',
    'long_description': '# Bumblebee\n\n![Bumblebee image](./docs/bumblebee.png)\n\n## Install\n\n```\npip install eyecu_bumblebee\n```\n\n## Our Website\n\n[EyeCU Vision](https://eyecuvision.com/) \\\n[EyeCU Future](https://eyecufuture.com/) \n\n\n## Example\n\n```python\nfrom bumblebee import *\n\nif __name__ == "__main__":\n    \n    VIDEO_PATH = "/path/to/video.mp4"\n\n    # Create a source\n    file_stream = sources.FileStream(VIDEO_PATH)\n\n    # Add an effect\n    goto = effects.GoTo(file_stream)\n\n    # Add some transformers\n    data = transformers.GrayScale(file_stream)\n    data = transformers.Normalization(data)\n\n    END_OF_VIDEO = file_stream.get_duration()\n    goto(END_OF_VIDEO)\n\n    # Create a dataset\n    single_frame = datasets.SingleFrame(data)\n\n    last_frame = single_frame.read()\n\n```\n\n## Architecture Diagram\n\n![Architecture](docs/bumblebee_arch_diagram.png)\n\n',
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Eye-C-U/bumblebee/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
