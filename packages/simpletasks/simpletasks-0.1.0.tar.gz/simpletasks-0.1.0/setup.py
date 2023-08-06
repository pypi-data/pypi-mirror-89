# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpletasks']

package_data = \
{'': ['*']}

extras_require = \
{'click': ['click>=7.1.2,<8.0.0'], 'tqdm': ['tqdm>=4.54.1,<5.0.0']}

setup_kwargs = {
    'name': 'simpletasks',
    'version': '0.1.0',
    'description': 'A simple library to run one task, or multiples ones in sequence or parallel',
    'long_description': '# simpletasks\n\nSimple tasks runner for Python\n\n\n----\nContributing\n\n```\npoetry install --no-root\npoetry install -E click -E tqdm\n```',
    'author': 'Thomas Muguet',
    'author_email': 'thomas.muguet@upowa.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/upOwa/simpletasks',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
