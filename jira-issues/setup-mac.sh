#!/usr/bin/env bash
#
# A shell script to set up the pre-requisites on a Mac
#

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

# 2. Install the Python version required by this script by running
# 3. Install uv

# Ensure we are in the directory of this script
SCRIPT_DIR="$(dirname "$0")"
pushd "$SCRIPT_DIR" >/dev/null
pyenv install --skip-existing
pip install --upgrade pip
pip install uv
popd >/dev/null
echo -e '\nTo run the Create Jira Issues script (see README.md for more detail):\n'
echo -e '1. Save your Jira issues to a CSV file.'
echo -e '2. Ensure you have a Jira API token handy.'
echo -e "3. Ensure you're in the script directory - \"cd $(realpath "$SCRIPT_DIR")\"."
echo -e '4. Use command: "uv run create-jira-issues.py"\n'

# Create a bash script which can be double-clicked to open a terminal and run the script
# This is a convenience for users who may not be comfortable using the terminal
LAUNCHER_SCRIPT="launch-create-jira-issues-mac.sh"
cat <<EOF >"$LAUNCHER_SCRIPT"
#!/usr/bin/env bash
# A script to launch the Create Jira Issues script in a new terminal window
osascript <<EOD
tell application "Terminal"
    do script "cd \"$(realpath "$SCRIPT_DIR")\" && uv run create-jira-issues.py"
    activate
end tell
EOD
EOF

# Make the macOS launcher executable
chmod +x "$LAUNCHER_SCRIPT"
