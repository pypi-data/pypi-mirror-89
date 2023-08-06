# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'peb',
    'version': '0.0.1',
    'description': '',
    'long_description': '# PEB\n\nPEB is python extensions.',
    'author': 'joyongjin',
    'author_email': 'wnrhd114@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joyongjin/peb',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
