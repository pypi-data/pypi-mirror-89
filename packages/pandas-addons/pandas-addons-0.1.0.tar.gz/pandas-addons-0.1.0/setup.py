# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_addons', 'pandas_addons.addons']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.25']

setup_kwargs = {
    'name': 'pandas-addons',
    'version': '0.1.0',
    'description': 'Extending pandas with new accessors',
    'long_description': None,
    'author': 'Clement Walter',
    'author_email': 'clement0walter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
