# Jira Issue Creation Script

This script takes a CSV of Jira issues and creates them on a Jira instance.

## Pre-Requisites

If you are a Mac user, you can try using the `setup-mac.sh` script.

Otherwise, the steps are:

1. a. Ensure `pyenv` is installed. On Mac, this can be installed using [Homebrew](https://brew.sh/) - i.e. `brew install pyenv`.

   b. Install tcl-tk for GUI. On Mac, this can be installed using [Homebrew](https://brew.sh/) - i.e. `brew install tcl-tk`. (Optional)

2. Install the Python version required by this script by running (from this directory):
   `pyenv install`. Check that the `python --version` and `pip --version` match the contents of the `.python-version` file.

3. Install `uv` dependency manager. Once `pyenv` has installed the required Python, run: `pip install uv`.

## Usage

Export your Jira issues to a CSV. Save it somewhere memorable.  The default location is `jira-issues.csv` in this directory.  A template is provided in the `resources` directory.

You'll need an [API token for SKAO Jira](https://jira.skatelescope.org/plugins/servlet/de.resolution.apitokenauth/admin).

You can set your Jira API token as an environment variable, if you don't want to enter it each time you run the script:

`export JIRA_API_TOKEN=[YOUR_API_TOKEN]`

To run the script:

1. Save your Jira issues to a CSV file.
2. Ensure you have a Jira API token handy.
3. Change to the `jira-issues` directory.
4. Use command: `uv run create_jira_issues.py`

## Development

You can ensure that code is linted, formatted and type-checked using pre-commit by installing the pre-commit hooks like:

`uv run pre-commit install`
