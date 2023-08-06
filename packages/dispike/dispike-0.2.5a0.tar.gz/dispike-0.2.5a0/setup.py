# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dispike',
 'dispike.helper',
 'dispike.middlewares',
 'dispike.models',
 'dispike.models.discord_types']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'httpx>=0.16.1,<0.17.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.7.3,<2.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'uvicorn>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'dispike',
    'version': '0.2.5a0',
    'description': '',
    'long_description': None,
    'author': 'Mustafa Mohamed',
    'author_email': 'ms7mohamed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
