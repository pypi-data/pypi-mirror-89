# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keynote_highlight']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.3,<3.0.0',
 'black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'pyperclip>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['keyhi = keynote_highlight.main:main']}

setup_kwargs = {
    'name': 'keynote-highlight',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Nikita Churikov',
    'author_email': 'nikita@chur.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
