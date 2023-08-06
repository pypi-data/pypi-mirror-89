# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_notifier']

package_data = \
{'': ['*']}

install_requires = \
['python-telegram-bot>=13.1,<14.0', 'telebot>=0.0.4,<0.0.5']

entry_points = \
{'console_scripts': ['pre_notifier = pre_notifier.pre_notifier:main']}

setup_kwargs = {
    'name': 'pre-notifier',
    'version': '0.1.13',
    'description': 'This tool provides you ability to send yourself information about looong executed command when it is done. Information will be sent using Telegram Bot, which you can generate for yourself with Telegram BotFather.',
    'long_description': "# Notifier\n\nThis tool provides you ability to send yourself information about looong executed command when it is done. Information will be sent using Telegram Bot, which you can generate for yourself with Telegram BotFather.\n\n\n## Prerequisites\n1. First of all register your bot at [@BotFather](https://telegram.me/BotFather). He will give you back your bot Telegram TOKEN. We'll use it later\n\n2. Get your Telegram ID. You can get it from [@userinfobot](https://telegram.me/userinfobot). Save it too.\n\n## Installation and running\n```shell\n>>> pip install pre_notifier\n>>> pre_notifier config --telegram_id=YOUR_TELEGRAM_ID --token=YOUR_BOT_TOKEN\n>>> pre_notifier notify [your_command_here]\n```\n",
    'author': 'Ivan Kuznetsov',
    'author_email': 'tikerlade@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
