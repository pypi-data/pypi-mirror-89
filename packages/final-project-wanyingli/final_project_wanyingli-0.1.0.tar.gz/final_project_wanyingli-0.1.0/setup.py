# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['final_project_wanyingli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'final-project-wanyingli',
    'version': '0.1.0',
    'description': 'Python package that returns the total country lending projects from the World Bank and the Asian Development Bank.',
    'long_description': None,
    'author': 'Wanyingli',
    'author_email': 'wl2722@columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
