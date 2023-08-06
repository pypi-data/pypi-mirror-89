# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cached_property']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'com.wyattbaldwin.cached-property',
    'version': '1.0.post1',
    'description': '@cached_property',
    'long_description': None,
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wylee/com.wyattbaldwin/tree/dev/cached_property',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
