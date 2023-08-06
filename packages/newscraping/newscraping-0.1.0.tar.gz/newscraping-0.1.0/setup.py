# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newscraping',
 'newscraping.application',
 'newscraping.infrastructure',
 'newscraping.settings']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'pandas>=1.2.0,<2.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['news = newscraping.application.scraping:news']}

setup_kwargs = {
    'name': 'newscraping',
    'version': '0.1.0',
    'description': 'Web scraping of financial headlines',
    'long_description': None,
    'author': 'Jerome Blin',
    'author_email': 'blinjrm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
