# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyramid_resourceful']

package_data = \
{'': ['*']}

install_requires = \
['pyramid']

extras_require = \
{':python_version == "3.6"': ['dataclasses']}

setup_kwargs = {
    'name': 'pyramid-resourceful',
    'version': '1.0a2',
    'description': 'Resourceful routes & views for Pyramd',
    'long_description': 'pyramid_resourceful\n+++++++++++++++++++\n\n``pyramid_resourceful`` is a somewhat-opinionated toolkit for building\nresourceful Web services and applications on top of the Pyramid Web\nframework.\n\nTake a look in the ``examples`` directory for self-contained, runnable\nexamples.\n\nSee https://pyramid-resourceful.readthedocs.io/ for detailed documentation\nof interfaces, APIs, and usage.\n\nLicense\n=======\n\nThis package is provided under the MIT license. See the ``LICENSE`` file\nfor details.\n',
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wylee/pyramid_resourceful',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
