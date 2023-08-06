# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_notifier']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pre-notifier',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Ivan Kuznetsov',
    'author_email': 'tikerlade@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
