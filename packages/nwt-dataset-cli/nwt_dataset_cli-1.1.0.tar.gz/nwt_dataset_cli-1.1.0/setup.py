# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nwt_dataset_cli', 'nwt_dataset_cli.helpers', 'nwt_dataset_cli.services']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.3,<2.0.0',
 'pymongo>=3.11.0,<4.0.0',
 'sklearn>=0.0,<0.1',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['nwt-dataset-cli = nwt_dataset_cli.app:app']}

setup_kwargs = {
    'name': 'nwt-dataset-cli',
    'version': '1.1.0',
    'description': 'Dataset Generate CLI',
    'long_description': '[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-386/)\n[![Poetry 1.0.10](https://img.shields.io/badge/poetry-1.0.10-blue.svg)](https://github.com/sdispater/poetry/releases/tag/1.0.10)\n\n# dataset-cli\n\n## Getting started\n\nThis project uses:\n\n- [poetry](https://python-poetry.org/) as dependency manager\n- [mypy](http://mypy-lang.org/) for static typing analysis\n- [black](https://black.readthedocs.io/) for code formatting\n- [flake8](http://flake8.pycqa.org/) for linting\n- [pytest](https://docs.pytest.org/) as testing framework\n- [coverage](https://coverage.readthedocs.io/) for code coverage reporting\n- [pre-commit](https://pre-commit.com/) to setup git hooks (formatting and linting before commits)\n\n```sh\n# Clone the repository\ngit clone git@bitbucket.org:newtralmedia/dataset-cli-lib\n\n# Install the dependencies using poetry\npoetry install\n\n# Enable virtual environment\npoetry shell\n\n# Setup pre commit hooks\npoetry run pre-commit install\npoetry run pre-commit run --all-files\n\n# If you need create a tunel ssh to connect to remote mongo\nssh -i key.pem user@remotehost -L 27017:localhost:27017 -N\n```\n\n## Cli Commands\n\n```sh\n# Commands\ncreate    Create a dataset with custom parameters.\nfromjson  Create a dataset from json file.\n\n# Show all options for command\npython dataset_cli/app.py create --help\npython dataset_cli/app.py fromjson --help\n\n# Create dateset from cli\npython dataset_cli/app.py create --start 2018-09-24 --target fact --source slack --random 123\n\n# Create dateset from json\npython dataset_cli/app.py fromjson --file xxxxxx.json\n\n# Custom mongo uri\npython dataset_cli/app.py fromjson --mongo mongodb://remote_host:27017 --file xxxxxxx.json\n\n# Folder to export dataset\npython dataset_cli/app.py create --target fact --source editor --random 123 --folder my_folder\n```\n\n## Release\n\nIn order to generate a new release you will need:\n\n**Node LTS**\n\n```sh\ncurl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash\nnvm install lts # You may need to open a new shell\n```\n\n**[standard-version](https://www.npmjs.com/package/standard-version)**\n\n```sh\nnpm install --global standard-version\n```\n\nJust run the following script. It will:\n\n- Checkout to master\n- Merge the most recent develop changes\n- Update package version and create a new tag\n- Push changes to master and develop\n\n```sh\n./scripts/release\n```\n\n## Test\n\nRun every tests\n\n```sh\npoetry run pytest\n```\n\n## Coverage\n\nRun tests and generate a code coverage report\n\n```sh\npoetry run coverage run -m pytest\npoetry run coverage report -m\n\n# Remove a previously generated coverage reports\npoetry run coverage erase\n```\n',
    'author': 'Pablo Alvarez',
    'author_email': 'pablo.alvarez@newtral.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bitbucket.org/newtralmedia/dataset-cli-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
