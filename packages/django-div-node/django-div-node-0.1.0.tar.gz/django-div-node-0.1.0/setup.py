# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_div_node']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.1,<3.2']

setup_kwargs = {
    'name': 'django-div-node',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
