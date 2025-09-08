# Jira Issue Creation Script

This script takes a CSV of Jira issues and creates them on a Jira instance.

## Pre-Requisites

1. a. Ensure `pyenv` is installed. On Mac, this can be installed using [Homebrew](https://brew.sh/) - i.e. `brew install pyenv`.

   b. Install tcl-tk for GUI. On Mac, this can be installed using [Homebrew](https://brew.sh/) - i.e. `brew install tcl-tk`. (Optional)

2. Install the Python version required by this script by running (from this directory):
   `pyenv install`. Check that the `python --version` and `pip --version` match the contents of the `.python-version` file.
3. Install `uv` dependency manager. Once `pyenv` has installed the required Python, run: `pip install uv`.
4. Create a virtual env with the dependencies: `uv install`

## Usage

Export your Jira issues to a CSV. Save it somewhere memorable.  The default location is `jira-issues.csv` in this directory.

To run the script:

`uv run ./create_jira_issues.py`

## Development

You can ensure that code is linted, formatted and type-checked using pre-commit by installing the pre-commit hooks like:

`uv run pre-commit install`
