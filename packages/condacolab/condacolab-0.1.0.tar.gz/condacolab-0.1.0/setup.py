# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['condacolab']
setup_kwargs = {
    'name': 'condacolab',
    'version': '0.1.0',
    'description': 'Install Conda and friends on Google Colab, easily',
    'long_description': None,
    'author': 'Jaime Rodríguez-Guerra',
    'author_email': 'jaimergp@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaimergp/condacolab',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
