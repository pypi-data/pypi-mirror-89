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
    'version': '1.0.post2',
    'description': '@cached_property',
    'long_description': '# Cached Property\n\nProvides a thread safe `@cached_property` decorator that can be used\nin place of the built in `@property` decorator for properties that are\nexpensive to compute or that aren\'t expected to change over the lifetime\nof an instance.\n\n## Usage\n\n    >>> from cached_property import cached_property\n    >>> class MyClass:\n    ...     @cached_property\n    ...     def prop(self):\n    ...         return 2 ** 42\n    ...\n    >>> instance = MyClass()\n    >>> "prop" in instance.__dict__\n    False\n    >>> instance.prop  # value computed and cached\n    4398046511104\n    >>> "prop" in instance.__dict__\n    True\n    >>> instance.prop  # cached value returned directly\n    4398046511104\n',
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
