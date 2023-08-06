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
    'version': '0.1.2',
    'description': 'colab miscellaneous utils',
    'long_description': '# colab miscellaneous utils [![Codacy Badge](https://app.codacy.com/project/badge/Grade/83b7b2cb3ade4589812917f187a8abab)](https://www.codacy.com/gh/ffreemt/colab-misc-utils/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/colab-misc-utils&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/clmutils.svg)](https://badge.fury.io/py/clmutils)\nMiscellaneous utils mainly intended for use in colab\n\n## Demo: notebooks in Colab\n### `git push` from Colab\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1n0agOGg8rBoR0Ld3WAvh20QzXeZZ7xCk?usp=sharing)\n### Set up a reverse ssh tunnel for ssh to Colab VM\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1CIstRNIZjKhMqCch-FRyoIoiFjGAOGii?usp=sharing)\nin English (I may provide a Chinese version later)\n\n\n## Installation\n```bash\npip install clmutils  # clm: colab-misc\n```\n\n## Usage\n### Write a private key to `~/.ssh/gh-key`\n```python\nfrom clmutils import create_file\ngh_key = \\\n"""\n-----BEGIN EC PRIVATE KEY-----\nMH.............................................................9\nAwEHoUQDQgAEoLlGQRzIVHYw3gvC/QFw3Ru45zGawaBaCq6jTqdyH2Kp8zIB3TdJ\nK9ztlJBRRAOHh5sPhQ4QpdZH1v1rWeDWIQ==\n-----END EC PRIVATE KEY-----\n""".strip() + "\\n"\n# Do not remove .strip() + "\\n"\n# the private key is very picky about format\n\ncreate_file(gh_key, dest="~/.ssh/gh-key")\n```\n### Set up `github.com` config for `git push`\n```python\nfrom clmutils import append_content\nconfig_github_entry = \\\n"""\nHost github.com\n   HostName github.com\n   User git\n   IdentityFile ~/.ssh/gh-key\n"""\nappend_content(config_github_entry, dest="~/.ssh/config")\n```\nVerify that everything is OK, from a cell\n```ipynb\n!ssh -o StrictHostKeyChecking=no -T git@github.com\n```\nIf you see something similar to\n```bash\nHi your-name! You\'ve successfully authenticated, but GitHub does not provide shell access.\n```\nyou are good to go.\n\nYou can now set up `git config global` from a cell, e.g.\n```ipynb\n!git config --global user.email your-email-address\n!git config --global user.name your-github-username\n# !ssh-keyscan github.com >> ~/.ssh/known_hosts\n```\nYou are ready to clone your own repo, run your app and generate new data, update the repo and push to `github`.\n\n## Utils planned\n* :white_check_mark: `create_file`\n  creates a file with given mode, e.g. for `.ssh/id_rsa` or `IdentityFile` in `.ssh/config`\n\n* :white_check_mark: `apppend_content`\n appends some content to a file, e.g., for appended a public key to `.ssh/authorized_keys`\n\n* :white_check_mark: `chmod600`\n   `chmod` of a file\n\n*  `reverse_ssh_tunnel`\n sets up a reverse ssh tunnel to a remote host with via autossh\n\n*  More',
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
