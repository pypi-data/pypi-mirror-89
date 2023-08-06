# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_quote_generator']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=2.10.1,<3.0.0']

setup_kwargs = {
    'name': 'random-quote-generator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jan Giacomelli',
    'author_email': 'jan@typless.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
