# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plus', 'plus.data', 'plus.model']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17.4,<2.0.0',
 'pandas>=1.1.1,<2.0.0',
 'pillow>=7.0.0,<8.0.0',
 'scikit-learn>=0.22.1,<0.23.0',
 'scipy>=1.4.1,<2.0.0',
 'torch>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'bio-embeddings-plus',
    'version': '0.1.0',
    'description': 'Protein sequence representations Learned Using Structural information (https://arxiv.org/abs/1912.05625)',
    'long_description': None,
    'author': 'Seonwoo Min',
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
