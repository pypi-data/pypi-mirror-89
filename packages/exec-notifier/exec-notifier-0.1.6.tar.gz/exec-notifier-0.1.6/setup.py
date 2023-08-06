# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['exec_notifier']
entry_points = \
{'console_scripts': ['exec_notifier = exec_notifier:main']}

setup_kwargs = {
    'name': 'exec-notifier',
    'version': '0.1.6',
    'description': 'Tool to notify you when command will be executed.',
    'long_description': '# Notifier\nThis tool provides you ability to send yourself information about looong executed command when it is done. Information will be sent using Telegram Bot, which you can generate for yourself with Telegram BotFather.\n\n## Installation and running\n```shell\n>>> pip install pre_notifier\n>>> pre_notifier config --telegram_id=YOUR_TELEGRAM_ID --token=YOUR_BOT_TOKEN\n>>> pre_notifier notify [your_command_here]\n```',
    'author': 'Ivan Kuznetsov',
    'author_email': 'tikerlade@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
