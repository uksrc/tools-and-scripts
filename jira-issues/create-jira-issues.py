#!/usr/bin/env -S uv run --script
import csv
import json
import logging
import os
from getpass import getpass

from jira import JIRA, JIRAError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

jira_domain = "https://jira.skatelescope.org"


try:
    from tkinter import filedialog as fd

    csv_filename = fd.askopenfilename(
        title="Select CSV file with Jira issues", filetypes=[("CSV files", "*.csv")]
    )
except ImportError:
    # Fallback for environments without tkinter (e.g., command line)
    csv_filename = (
        input("Enter the path to the CSV file with Jira issues (./jira-issues.csv): ")
        or "./jira-issues.csv"
    )

user_name = input("Enter your Jira username (First.Last): ")

if api_token := os.getenv("JIRA_API_TOKEN"):
    use_api_token_env_var = input("Use env var JIRA_API_TOKEN? (Y/n): ")

if not api_token or use_api_token_env_var.lower() == "n":
    api_token = getpass("Enter your Jira API token: ")

try:
    jira = JIRA(jira_domain, basic_auth=(user_name, api_token))
except JIRAError as e:
    logger.error(f"Failed to connect to Jira: {e}")
    logger.error("Please check your username and API token.")
    exit(1)

with open(csv_filename, newline="", encoding="utf-8-sig") as csv_file:
    reader = csv.DictReader(csv_file)
    logger.debug(f"CSV file opened: {csv_filename}")
    logger.debug(f"CSV headers: {reader.fieldnames}")
    logger.debug("CSV rows:")
    for row in reader:
        logger.debug(f"Processing row: {row}")
        issue_payload = {
            "project": {"key": row["Project Key"]},
            "summary": row["Summary"],
            "description": row["Description"],
            "issuetype": {"name": row["Issue Type"]},
            "customfield_11122": row["Acceptance Criteria"],
            "customfield_10002": int(row["Story Points"])
            if row["Story Points"]
            else None,
            "fixVersions": [{"name": row["Fix Versions"]}],
            "customfield_11703": {"value": row["Due Sprint"]} if row["Due Sprint"] else None,
            "priority": {"name": row["Priority"]},
            "labels": row["Labels"].split(",") if row["Labels"] else [],
            "customfield_11949": row["Outcomes"],
            "assignee": {"name": row["Assignee"]},
            "customfield_10006": row["Epic Link"],
        }
        logger.debug(f"Issue payload: {json.dumps(issue_payload, indent=2)}")
        # Create the issue in Jira
        new_issue = jira.create_issue(fields=issue_payload)
        logger.info(f"Issue created: {new_issue.key} with summary: {row['Summary']}")
