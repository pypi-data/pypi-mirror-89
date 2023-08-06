# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tracktrace', 'tracktrace.ocean', 'tracktrace.rail']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'bs4>=0.0.1,<0.0.2',
 'feedparser>=6.0.2,<7.0.0',
 'html5lib>=1.1,<2.0',
 'lxml>=4.6.1,<5.0.0',
 'pandas>=1.1.4,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'tracktrace',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Dhruv Kar',
    'author_email': 'dhruv@wints.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
