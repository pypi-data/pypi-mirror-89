# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smithsonian_api_queri']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.5,<2.0.0']

setup_kwargs = {
    'name': 'smithsonian-api-queri',
    'version': '0.1.0',
    'description': 'Python package designed to query data from the Smithsonian Open Access API using category filters based on user input.',
    'long_description': None,
    'author': 'Alys-217',
    'author_email': 'ajz2123@tc.columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
