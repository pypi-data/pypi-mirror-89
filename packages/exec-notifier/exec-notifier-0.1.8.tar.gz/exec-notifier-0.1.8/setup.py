# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['exec_notifier']
entry_points = \
{'console_scripts': ['exec_notifier = exec_notifier:main']}

setup_kwargs = {
    'name': 'exec-notifier',
    'version': '0.1.8',
    'description': 'Tool to notify you when command will be executed.',
    'long_description': '# Execution Notifier :speech_balloon:\n[![PyPI](https://img.shields.io/pypi/v/exec-notifier)](https://pypi.org/project/exec-notifier/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Actions Status](https://github.com/tikerlade/exec-notifier/workflows/Deploy%20publisher/badge.svg)](https://github.com/tikerlade/exec-notifier/actions/)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tikerlade/exec-notifier/master.svg)](https://results.pre-commit.ci/latest/github/tikerlade/exec-notifier/master)\n\nThis tool provides you ability to send yourself information about looong executed command when it is done. Information will be sent using Telegram Bot, which you can generate for yourself with Telegram BotFather.\n\n## Prerequisites :bookmark_tabs:\nIn execution of your application you will need your Telegram ID. To get it visit [@exec_notifier_bot](https://telegram.me/exec_notifier_bot) and use `/start` command.\n\n## Installation and running\n```shell\n>>> pip install exec-notifier\n>>> exec_notifier config --telegram_id=YOUR_TELEGRAM_ID\n>>> exec_notifier notify [your_command_here]\n```\n\n## Future :soon:\n* Your own bot supportage will be added\n',
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
