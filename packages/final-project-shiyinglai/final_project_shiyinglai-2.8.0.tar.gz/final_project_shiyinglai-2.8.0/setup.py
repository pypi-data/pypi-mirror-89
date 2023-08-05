# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['final_project_shiyinglai']

package_data = \
{'': ['*']}

install_requires = \
['datetime>=4.3,<5.0',
 'matplotlib>=3.3.3,<4.0.0',
 'pandas>=1.1.5,<2.0.0',
 'pillow==8.0.0',
 'requests>=2.25.1,<3.0.0',
 'urllib3==1.23']

setup_kwargs = {
    'name': 'final-project-shiyinglai',
    'version': '2.8.0',
    'description': 'This is an API client for HAM.',
    'long_description': None,
    'author': 'Shiying Lai',
    'author_email': 'sl4849@columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
