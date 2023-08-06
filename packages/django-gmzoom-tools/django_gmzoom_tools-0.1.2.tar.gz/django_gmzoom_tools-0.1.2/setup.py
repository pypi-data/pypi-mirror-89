# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_gmzoom_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-gmzoom-tools',
    'version': '0.1.2',
    'description': 'Slotmarks.com - online casino guide',
    'long_description': '[Slotmarks.com](https://slotmarks.com/en/) - your guide to online casinos.\n\n#New Casinos\n\n',
    'author': 'slotmarks',
    'author_email': 'info@slotmarks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://slotmarks.com/en/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.2,<4.0',
}


setup(**setup_kwargs)
