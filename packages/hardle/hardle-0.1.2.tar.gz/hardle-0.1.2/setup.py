# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hardle']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hardle = hardle.__main__:main']}

setup_kwargs = {
    'name': 'hardle',
    'version': '0.1.2',
    'description': 'Download content from .HAR files',
    'long_description': '# Hardle\n\nA simple & lightweight utility for (synchronously) downloading content from .HAR files. Useful when you want to download static sites for offline use.\n\n## Installation\n\n```\n$ pip3 install hardle\n```\n\nHardle uses type annotations, so Python 3.5 (minimum) is required.\n\n## Usage\n\n### From the Command Line\n\n```\n$ hardle path/to/file.har out/\n```\n\n### From Python\n\n```py\nfrom hardle import download\n\ndownload("path/to/file.har", "out/")\n```\n\n## License\n\n[MIT](./LICENSE)\n',
    'author': 'docyx',
    'author_email': 'oliverxur@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/docyx/hardle',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
