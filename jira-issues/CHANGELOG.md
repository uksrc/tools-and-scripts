# Create Jira Issues Script

A script to generate Jira tickets from the rows of a spreadsheet.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.1 - 2025-09-16

### Fixed

- Allow an empty Due Sprint field in the source CSV.  The field will not be set.
- Allow an empty Priority field in the source CSV - default to "Low".

## 1.0.0 - 2025-09-09

### Added

- Python script to parse a CSV of issue details and POST them to Jira.
- An optional GUI file-picker to select the CSV source file.
- A GitHub workflow to package and publish releases of the script.
- A convenience script to set-up pre-requisites on a Mac.
