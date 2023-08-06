# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pikas', 'pikas.ensemble', 'pikas.ensemble.tests']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=0.24.0,<0.25.0']

setup_kwargs = {
    'name': 'pikas',
    'version': '0.1.0',
    'description': 'A machine learning framework for exploring tree ensemble algorithms.',
    'long_description': None,
    'author': 'Stephanos Stephani',
    'author_email': 'stephanos.stephani@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
