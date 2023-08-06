# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whistling']

package_data = \
{'': ['*']}

install_requires = \
['contextvars>=2.4,<3.0', 'httpx>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'whistling',
    'version': '0.1.0',
    'description': 'A collection of functions to report a malicious URL',
    'long_description': '# whistling\n\nWhistling is a Python package to report malicious / suspicious URL.\n\nThe following services are supported.\n\n- Google Safe Browsing\n- APWG eCX\n- Netcraft\n- urlscan.io\n',
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
