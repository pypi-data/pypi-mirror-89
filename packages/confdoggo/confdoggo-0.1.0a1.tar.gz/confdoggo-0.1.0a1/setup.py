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
    'version': '0.1.0a1',
    'description': 'Your personal configuration doggo.',
    'long_description': '# confdoggo 🐶\n\nDefine your builtin settings:\n\n```python\nclass MySettings(confdoggo.Settings):\n    class _(confdoggo.Settings):\n        host: str = "localhost"\n        port: int = 8080\n    server = _()\n\n    class _(confdoggo.Settings):\n        x: int = 42\n    client = _()\n\n    reload_on_changes = True\n    scheduled_shutdown: datetime = None\n```\n\nLet confdoggo catch the configuration files, and run extensible type checking:\n\n```python\nsettings = confdoggo.go_catch(\n    MySettings,\n    [\n        \'file://./simple.json\',  # a local file\n        Path(\'.\') / \'another_one.yaml\',  # another local file\n        \'ftp://192.168.1.1/folder/file.json\',  # a remote file\n        \'https://192.168.1.2/folder/file.ini\',  # another remote file\n    ],\n)\n```\nNote: order matters! Configurations that have a higher index have higher importance.\n\nAccess configuration easily:\n\n```python\nassert settings.server.port == 8080 \n```\n\nSee a full example [here](./examples/simple.py).\n\n\n## Install\n\n```bash\n$ pip install confdoggo\n```\n\n\n## Under development\n\nThis project is under development: expect breaking changes!\n',
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
