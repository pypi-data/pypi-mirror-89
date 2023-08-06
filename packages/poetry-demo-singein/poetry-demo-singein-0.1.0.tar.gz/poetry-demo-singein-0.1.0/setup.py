# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_singein']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.1.4,<4.0.0', 'pendulum>=2.1.2,<3.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'poetry-demo-singein',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Singein',
    'author_email': 'singein@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
