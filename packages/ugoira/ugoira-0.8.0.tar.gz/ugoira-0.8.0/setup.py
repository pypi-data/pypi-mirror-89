# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ugoira']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'click>=7.1.2,<8.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'requests>=2.25.1,<3.0.0']

extras_require = \
{'apng': ['apng>=0.3.4,<0.4.0']}

entry_points = \
{'console_scripts': ['ugoira = ugoira.cli:ugoira']}

setup_kwargs = {
    'name': 'ugoira',
    'version': '0.8.0',
    'description': 'ugoira for download pixiv ugoira images',
    'long_description': None,
    'author': 'Kim Jin Su',
    'author_email': 'item4_hun@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
