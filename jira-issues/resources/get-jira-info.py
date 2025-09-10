#!/usr/bin/env python3
import logging
import os
from getpass import getpass
from typing import Any

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Configure logging to show INFO level messages
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_jira_auth() -> tuple[str, HTTPBasicAuth]:
    jira_domain = input("Enter your Jira domain (e.g., your-domain.atlassian.net): ")
    email = input("Enter your Jira email: ")
    api_token = getpass("Enter your Jira API token: ")
    return jira_domain, HTTPBasicAuth(email, api_token)


def get_project_issue_types(
    jira_domain: str, auth: HTTPBasicAuth, project_key: str
) -> list[str]:
    url = f"https://{jira_domain}/rest/api/2/project/{project_key}"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    data = response.json()
    return [issue_type["name"] for issue_type in data["issueTypes"]]


def get_example_issue_key(
    jira_domain: str, auth: HTTPBasicAuth, project_key: str, issue_type: str
) -> str | None:
    jql = f"project={project_key} AND issuetype={issue_type}"
    url = f"https://{jira_domain}/rest/api/2/search"
    params = {"jql": jql, "maxResults": "1"}
    response = requests.get(url, auth=auth, params=params)
    response.raise_for_status()
    issues = response.json().get("issues", [])
    return issues[0]["key"] if issues else None


def get_issue_fields(jira_domain: str, auth: HTTPBasicAuth, issue_key: str) -> Any:
    url = f"https://{jira_domain}/rest/api/2/issue/{issue_key}?expand=names"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()["names"]


def get_all_fields(jira_domain: str, auth: HTTPBasicAuth) -> Any:
    url = f"https://{jira_domain}/rest/api/2/field"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()


def translate_field_type(field_type: str) -> str:
    translation_map = {
        "option": "Select List (single choice) or Checkbox",
        "user": "User Picker",
        "string": "Text Field",
        "array": "Labels",
        "datetime": "Date Time Picker",
        "number": "Number Field",
        "date": "Date Picker",
        "team": "Team Field",
        "group": "Group Picker",
        "option-with-child": "Select List (cascading)",
    }
    return translation_map.get(field_type, "N/A")


def main() -> None:
    jira_domain, auth = get_jira_auth()
    project_key = input("Enter the project key: ")

    try:
        issue_types = get_project_issue_types(jira_domain, auth, project_key)
        logging.info(f"Issue types found: {issue_types}")

        example_issues = {}
        for issue_type in issue_types:
            issue_key = get_example_issue_key(
                jira_domain, auth, project_key, issue_type
            )
            if issue_key:
                example_issues[issue_type] = issue_key
                logging.info(f"Example issue for {issue_type}: {issue_key}")
            else:
                logging.warning(f"No example issue found for {issue_type}")

        custom_field_names = {}
        for issue_type, issue_key in example_issues.items():
            fields = get_issue_fields(jira_domain, auth, issue_key)
            custom_field_names.update(fields)

        all_fields = get_all_fields(jira_domain, auth)
        custom_fields_info = [
            {
                "Cloud URL": f"https://{jira_domain}",
                "Project Key": project_key,
                "Field ID": field["id"],
                "Field Name": custom_field_names.get(field["id"], field["name"]),
                "Field Type": field["schema"]["type"] if "schema" in field else "N/A",
                "Translated Field Type": translate_field_type(
                    field["schema"]["type"] if "schema" in field else "N/A"
                ),
            }
            for field in all_fields
            if field["id"].startswith("customfield_")
            and field["id"] in custom_field_names
        ]

        df = pd.DataFrame(custom_fields_info)
        csv_file = f"{project_key}_custom_fields.csv"
        df.to_csv(csv_file, index=False)
        absolute_path = os.path.abspath(csv_file)
        logging.info(f"Custom fields report generated and saved to {absolute_path}")

    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
