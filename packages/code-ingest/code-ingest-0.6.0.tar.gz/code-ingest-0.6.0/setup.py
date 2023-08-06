# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_ingest']

package_data = \
{'': ['*']}

install_requires = \
['docker', 'starlette', 'uvicorn']

entry_points = \
{'console_scripts': ['ingest_server = code_ingest.__main__:main',
                     'ingest_tests = tests.functionality_check:run_tests']}

setup_kwargs = {
    'name': 'code-ingest',
    'version': '0.6.0',
    'description': 'This runs code in a time-limited, offline docker container and returns the results.',
    'long_description': '# RACTF Code Ingest server\n\nThis is the code ingest and execution server for RACTF.\n\nThis runs code in a time-limited, offline docker container and returns the results.\n\nIt\'s written to meet a specific set of requirements and work in conjunction with a webapp front end.\n\n## Prerequsites & Setup\n\n- Python 3.9.1 or above with pip\n- Pyenv installed (optional)\n- Poetry installed\n- Linux distro, ideally something Debian/Ubuntu based\n- Docker [installed](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) on host\n\nIf you don\'t have the required python version (3.9.1 as of writing), install [pyenv](https://github.com/pyenv/pyenv#basic-github-checkout) with basic checkout.\nThen install the build dependencies, which is listed on the [wiki](https://github.com/pyenv/pyenv/wiki)\n\nAdd the following lines to your `~/.bashrc` file (assuming you haven\'t done so from the pyenv guide):\n\n```bash\n# Pyenv installation\n\nif [[ -z "$VIRTUAL_ENV" ]]; then\n    export PATH="$HOME/.pyenv/bin:$PATH"\n    eval "$(pyenv init -)"\nfi\n```\n\nIf you have a different shell, follow the pyenv install guide. Pyenv isn\'t mandatory if you have the correct version.\n\nNext, install [poetry](https://python-poetry.org/docs/) with their suggested way, as this is necessary for the installation.\n\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n```\n**Note**: Poetry requires `python` so if you don\'t have `python2` you can soft link `python3`: `sudo ln -sf $(which python3) /usr/local/bin/python`\n\n## Installation & Deployment\n\nClone the repo and change directory into it:\n\nBuilds are available from PyPi, just do `python3 -m pip install code-ingest`.\n\n> Deploy with `ingest_server` and run basic tests with `ingest_tests`.\n\nAlternatively if you want to install inside an env:\n\n```bash\ngit clone https://gitlab.com/ractf/code-ingest.git\ncd code-ingest\n\n# If you\'re deploying for production.\npoetry install --no-dev\npoetry shell\n\n# <Set your environment variables here>\n# Remove the docker image every time you want it to be rebuilt.\ndocker rmi sh3llcod3/code-ingest # If you\'ve not deployed in a while.\ningest_server\n\n# If you\'re interested in making changes.\npoetry install\npoetry shell\npython -m code_ingest\n```\n\nYou should be able to use any virtualenv realistically.\n\nThe full documentation of environment variables, endpoints, etc can be found in the [docs](docs/ingest.rst)\n\n## Issues\n\nIf you encounter a bug, please create an issue stating with as much possible detail:\n\n- Your set-up\n- The bug\n- Any steps taken\n',
    'author': 'RACTF Contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ractf/code-ingest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
