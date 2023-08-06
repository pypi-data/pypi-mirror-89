# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'guid',
    'version': '0.2.0',
    'description': 'Human friendly GUID/UUID library',
    'long_description': None,
    'author': 'Logi Leifsson',
    'author_email': 'logileifs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
