# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ses_log_handler']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'ses-log-handler',
    'version': '1.0.0',
    'description': 'Log messages to email via Amazon SES',
    'long_description': None,
    'author': 'Matt Pye',
    'author_email': 'pyematt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
