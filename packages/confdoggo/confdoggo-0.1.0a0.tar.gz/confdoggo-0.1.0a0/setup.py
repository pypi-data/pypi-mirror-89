# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confdoggo', 'confdoggo.clients', 'confdoggo.frontends', 'confdoggo.watchers']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1']

extras_require = \
{'fs-watcher': ['watchdog>=0.10.3,<0.11.0'], 'yaml': ['PyYAML>=5.3.1,<6.0.0']}

setup_kwargs = {
    'name': 'confdoggo',
    'version': '0.1.0a0',
    'description': 'Your personal configuration doggo.',
    'long_description': None,
    'author': 'Daniele Parmeggiani',
    'author_email': 'git@danieleparmeggiani.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
