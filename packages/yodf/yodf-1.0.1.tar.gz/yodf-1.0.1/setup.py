# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yodf']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'yodf',
    'version': '1.0.1',
    'description': "'Hello, World!' Forward Mode Autdiff library with Tensorflow 1.15 like interface.",
    'long_description': 'https://arxiv.org/abs/1502.05767',
    'author': 'Yogesh Ketkar',
    'author_email': 'yogimogi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yogimogi/yodf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
