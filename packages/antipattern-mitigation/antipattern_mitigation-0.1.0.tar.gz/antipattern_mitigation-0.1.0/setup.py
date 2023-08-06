# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['antipattern_mitigation', 'antipattern_mitigation.service']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'uvicorn>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'antipattern-mitigation',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ulfet',
    'author_email': 'ulfet.rwth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
