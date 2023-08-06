# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['example_package_yrf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'example-package-yrf',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yuri Fernandes',
    'author_email': 'fernandes.yuri.ironhide@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
