# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_framework_jwk',
 'rest_framework_jwk.management',
 'rest_framework_jwk.management.commands',
 'rest_framework_jwk.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django',
 'cryptography>=3.3.1,<4.0.0',
 'djangorestframework>=3.10,<4.0',
 'jwcrypto>=0.8,<0.9']

setup_kwargs = {
    'name': 'django-rest-framework-jwk',
    'version': '0.1.3',
    'description': 'Easy JSON Web Keys (JWK) for your Django project',
    'long_description': None,
    'author': 'Gustavo Maronato',
    'author_email': 'gustavo@maronato.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
