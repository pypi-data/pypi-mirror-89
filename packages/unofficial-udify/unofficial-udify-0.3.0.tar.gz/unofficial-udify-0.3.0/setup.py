# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udify',
 'udify.dataset_readers',
 'udify.models',
 'udify.modules',
 'udify.optimizers',
 'udify.predictors']

package_data = \
{'': ['*']}

install_requires = \
['allennlp>=1.0.0,<2.0.0', 'conllu>=3.0,<4.0', 'transformers>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'unofficial-udify',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Dan Kondratyuk',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
