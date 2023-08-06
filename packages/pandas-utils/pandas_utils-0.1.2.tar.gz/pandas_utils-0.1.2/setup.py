# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.5,<2.0.0']

setup_kwargs = {
    'name': 'pandas-utils',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'rschmidtner',
    'author_email': 'RSchmidtner@NewYorker.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
