# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smart_alpha', 'tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'smart-alpha',
    'version': '0.0.1',
    'description': 'Top-level package for Smart Alpha.',
    'long_description': '===========\nSmart Alpha\n===========\n\n\n.. image:: https://img.shields.io/pypi/v/smart_alpha.svg\n        :target: https://pypi.python.org/pypi/smart_alpha\n\n.. image:: https://img.shields.io/travis/amazingvince/smart_alpha.svg\n        :target: https://travis-ci.com/amazingvince/smart_alpha\n\n.. image:: https://readthedocs.org/projects/smart-alpha/badge/?version=latest\n        :target: https://smart-alpha.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/amazingvince/smart_alpha/shield.svg\n     :target: https://pyup.io/repos/github/amazingvince/smart_alpha/\n     :alt: Updates\n\n\n\nframework for trading stocks \n\n\n* Free software: Apache-2.0\n* Documentation: https://smart-alpha.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Vincent Haines',
    'author_email': 'amazingvince@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amazingvince/smart_alpha',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
