# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_cdk_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-cdk-utils',
    'version': '1.0.0',
    'description': 'Utilities to assist with building Python-based applications in AWS-CDK',
    'long_description': None,
    'author': 'Greg Farrow',
    'author_email': 'greg.farrow1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
