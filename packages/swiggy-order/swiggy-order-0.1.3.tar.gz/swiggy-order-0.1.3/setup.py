# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swiggy_order', 'swiggy_order.apis']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0,<16.0',
 'docopt>=0.6.2,<0.7.0',
 'prompt_toolkit>=3.0.8,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['order-food = swiggy_order:main']}

setup_kwargs = {
    'name': 'swiggy-order',
    'version': '0.1.3',
    'description': 'Order food via terminal.',
    'long_description': None,
    'author': 'Amresh Venugopal',
    'author_email': 'amresh.venugopal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
