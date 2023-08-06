# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlep']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mlep',
    'version': '0.1.1.dev1',
    'description': 'Interact with an EnergyPlus simulation during runtime using the BCVTB protocol.',
    'long_description': '# MLEP Client\nInteract with an EnergyPlus simulation during runtime using the BCVTB protocol.\n\n# Releasing\nSee [release info here](https://gist.github.com/corymosiman12/26fb682df2d36b5c9155f344eccbe404#releasing)\n',
    'author': 'Willy Bernal Heredia',
    'author_email': 'willy.bernalheredia@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
