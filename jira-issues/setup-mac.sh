#!/usr/bin/env bash
#
# A shell script to set up the pre-requisites on a Mac
#

#################
### Functions ###
#################

# Function to create launcher scripts
create_launcher_script() {
  local script_dir="$1"

  echo "Creating macOS launcher script..."
  local launcher_script="launch-create-jira-issues-mac.sh"
  cat <<EOF >"$launcher_script"
#!/usr/bin/env bash
# A script to launch the Create Jira Issues script in a new terminal window
osascript <<EOD
tell application "Terminal"
    do script "cd \"$(realpath "$script_dir")\" && uv run create-jira-issues.py"
    activate
end tell
EOD
EOF
  chmod +x "$launcher_script"
}

#########################################
### Main script execution starts here ###
#########################################

# 0. Check Brew installation and, if not present, install Brew
if ! command -v brew &>/dev/null; then
  echo "Homebrew not found. Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew is already installed."
fi

# 1. a. Ensure `pyenv` is installed. On Mac, this can be installed using [Homebrew](https://brew.sh/) - i.e. `brew install pyenv`.
if ! command -v pyenv &>/dev/null; then
  echo "pyenv not found. Installing pyenv..."
  brew install pyenv
else
  echo "pyenv is already installed."
fi

#    b. Install tcl-tk for GUI. On Mac, this can be installed using [Homebrew](https://brew.sh/) - i.e. `brew install tcl-tk`. (Optional)
if ! brew list tcl-tk &>/dev/null; then
  echo "tcl-tk not found. Installing tcl-tk..."
  brew install tcl-tk
else
  echo "tcl-tk is already installed."
fi

SCRIPT_DIR="$(dirname "$0")"
pushd "$SCRIPT_DIR" >/dev/null

# 2. Install the Python version required by this script by running
pyenv install --skip-existing

# 3. Install uv
pip install --upgrade pip
pip install uv

# 4. Create launcher scripts
create_launcher_script "$SCRIPT_DIR"

popd >/dev/null

echo -e '\nTo run the Create Jira Issues script (see README.md for more detail):\n'
echo -e '1. Save your Jira issues to a CSV file.'
echo -e '2. Ensure you have a Jira API token handy.'
echo -e '3. Run `launch-create-jira-issues-mac.sh` either from Finder or a terminal to run the script.'

# 5. Wait for user to press a key before closing the terminal window - useful if this script is run by double-clicking it in Finder
read -n 1 -s -r -p "Press any key to continue..."
echo
