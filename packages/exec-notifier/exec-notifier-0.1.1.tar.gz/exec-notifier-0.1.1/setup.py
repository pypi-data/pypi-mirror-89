# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['exec_notifier']
entry_points = \
{'console_scripts': ['pre_notifier = exec_notifier:main']}

setup_kwargs = {
    'name': 'exec-notifier',
    'version': '0.1.1',
    'description': 'Tool to notify you when command will be executed.',
    'long_description': None,
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
