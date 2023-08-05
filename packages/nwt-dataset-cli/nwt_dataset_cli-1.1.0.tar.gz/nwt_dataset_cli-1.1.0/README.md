[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-386/)
[![Poetry 1.0.10](https://img.shields.io/badge/poetry-1.0.10-blue.svg)](https://github.com/sdispater/poetry/releases/tag/1.0.10)

# dataset-cli

## Getting started

This project uses:

- [poetry](https://python-poetry.org/) as dependency manager
- [mypy](http://mypy-lang.org/) for static typing analysis
- [black](https://black.readthedocs.io/) for code formatting
- [flake8](http://flake8.pycqa.org/) for linting
- [pytest](https://docs.pytest.org/) as testing framework
- [coverage](https://coverage.readthedocs.io/) for code coverage reporting
- [pre-commit](https://pre-commit.com/) to setup git hooks (formatting and linting before commits)

```sh
# Clone the repository
git clone git@bitbucket.org:newtralmedia/dataset-cli-lib

# Install the dependencies using poetry
poetry install

# Enable virtual environment
poetry shell

# Setup pre commit hooks
poetry run pre-commit install
poetry run pre-commit run --all-files

# If you need create a tunel ssh to connect to remote mongo
ssh -i key.pem user@remotehost -L 27017:localhost:27017 -N
```

## Cli Commands

```sh
# Commands
create    Create a dataset with custom parameters.
fromjson  Create a dataset from json file.

# Show all options for command
python dataset_cli/app.py create --help
python dataset_cli/app.py fromjson --help

# Create dateset from cli
python dataset_cli/app.py create --start 2018-09-24 --target fact --source slack --random 123

# Create dateset from json
python dataset_cli/app.py fromjson --file xxxxxx.json

# Custom mongo uri
python dataset_cli/app.py fromjson --mongo mongodb://remote_host:27017 --file xxxxxxx.json

# Folder to export dataset
python dataset_cli/app.py create --target fact --source editor --random 123 --folder my_folder
```

## Release

In order to generate a new release you will need:

**Node LTS**

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
nvm install lts # You may need to open a new shell
```

**[standard-version](https://www.npmjs.com/package/standard-version)**

```sh
npm install --global standard-version
```

Just run the following script. It will:

- Checkout to master
- Merge the most recent develop changes
- Update package version and create a new tag
- Push changes to master and develop

```sh
./scripts/release
```

## Test

Run every tests

```sh
poetry run pytest
```

## Coverage

Run tests and generate a code coverage report

```sh
poetry run coverage run -m pytest
poetry run coverage report -m

# Remove a previously generated coverage reports
poetry run coverage erase
```
