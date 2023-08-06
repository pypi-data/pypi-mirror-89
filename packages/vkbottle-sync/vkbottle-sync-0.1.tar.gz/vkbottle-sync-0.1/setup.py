# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkbottle_sync']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.11,<4.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'choicelib>=0.1.1,<0.2.0',
 'vbml>=1.0,<2.0',
 'vkbottle-types>=0.1.21,<0.2.0',
 'watchgod>=0.6,<0.7']

setup_kwargs = {
    'name': 'vkbottle-sync',
    'version': '0.1',
    'description': 'Sync Version',
    'long_description': '# VKBottle Sync\n\n## Что это?\n\nВсе как в [vkbottle](https://github.com/timoniq/vkbottle) но синхронно\n',
    'author': 'timoniq',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vkbottle/sync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
