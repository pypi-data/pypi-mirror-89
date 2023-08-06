# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['http_log_parser']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['http-log-parser = http_log_parser:main']}

setup_kwargs = {
    'name': 'http-log-parser',
    'version': '0.1.0',
    'description': 'Cli tool to parse stream of http access events into json formatted events.',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
