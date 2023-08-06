# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crystal_eyes']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'fastapi>=0.62.0,<0.63.0',
 'numpy>=1.19.4,<2.0.0',
 'onnxruntime>=1.6.0,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'crystal-eyes',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'KiyoshiMu',
    'author_email': 'mooyewtsing@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
