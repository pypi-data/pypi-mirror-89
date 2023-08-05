# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clmutils']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'clmutils',
    'version': '0.1.1',
    'description': 'colab miscellaneous utils',
    'long_description': '# colab miscellaneous utils [![Codacy Badge](https://app.codacy.com/project/badge/Grade/83b7b2cb3ade4589812917f187a8abab)](https://www.codacy.com/gh/ffreemt/colab-misc-utils/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/colab-misc-utils&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/clmutils.svg)](https://badge.fury.io/py/clmutils)\nMiscellaneous utils mainly intended for use in colab\n\nUtils planned\n*  `create_file`\n  creates a file with given mode, e.g. for `.ssh/id_rsa` or `IdentityFile` in `.ssh/config`\n\n*  `apppend_content\n appends some content to a file, e.g., for appended a public key to `.ssh/authorized_keys`\n\n*  `chmod600`\n   `chmod` of a file\n\n*  reverse_ssh_tunnel\n sets up a reverse ssh tunnel to a remote host with via autossh\n\n*  More',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/colab-misc-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
