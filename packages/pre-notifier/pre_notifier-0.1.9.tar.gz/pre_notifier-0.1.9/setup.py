# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_notifier']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pre_notifier = pre_notifier.pre_notifier:main']}

setup_kwargs = {
    'name': 'pre-notifier',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'Ivan Kuznetsov',
    'author_email': 'tikerlade@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
