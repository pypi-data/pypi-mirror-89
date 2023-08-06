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
    'version': '0.1.1',
    'description': 'HTML custom div node in django template',
    'long_description': '# django-div-node\n\nHTML Div node in django template\n(only for internal use purpose)\n\n## USE AT YOUR OWN RISK\n\nYou can use pypi download this library: `django-div-node = "*"`\n\n',
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
