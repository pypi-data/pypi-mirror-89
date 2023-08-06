# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_notes', 'py_notes.utils']

package_data = \
{'': ['*'], 'py_notes.utils': ['databases/*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['notes = py_notes.notes:cli']}

setup_kwargs = {
    'name': 'py-notes',
    'version': '1.0.4',
    'description': 'Take notes directly in your terminal.',
    'long_description': "# notes-cli\n\nA Python based CLI for taking notes from your terminal. \n\nThis application was built using [Click](https://click.palletsprojects.com/), which is a wonderful Python package for building interactive CLIs. \n\n![Help Page Screenshot](https://imgur.com/vLY8omF.jpg)\n\n# Installation\n### PIP\nWe're published to [PyPI](https://pypi.org/project/py-notes/), which means you can install this package directly through Pip.\n\n`pip install py-notes`\n\n### Local\nYou must first clone this repository with:\n`git clone https://github.com/Saakshaat/notes-cli`\n\nThen, after `cd`ing into its directory, install the executable on your system with:\n`pip install --editable .`\n\nIf you don't want to have this installed globally, you can run it in a virtual environment. To create a virtual env, go to the repo's directory and on the top-level run\n- `virtualenv venv`\n- `. venv/bin/activate`\n- `pip install --editable .`\n\n# Running\n\nAfter installing the CLI successfully, you can run it from whichever environment you installed it in with\n\n`notes <command>` \n\n![show command demo](https://imgur.com/rVSe4Yp.jpg)\n\n The application uses a SQLite database to save notes in memory and maintains a threshold of (currently) 25 notes. \n \n When the total number of notes reaches the threshold, it deletes the oldest note in memory before adding the new note.",
    'author': 'Saakshaat',
    'author_email': 'saakshaat2001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Saakshaat/notes-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
