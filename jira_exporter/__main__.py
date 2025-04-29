import argparse
from config import load_config
from jira_client import fetch_issues
from extractors import extract_field, extract_issue_links, extract_links_flattened
from validators import evaluate_relation
from exporter import write_issues_to_csv, write_summary_csv
from requests.auth import HTTPBasicAuth


def main():
    parser = argparse.ArgumentParser(description="Export Jira issues to CSV.")
    parser.add_argument('--config', type=str, default='config.json', help='Path to the config file')
    args = parser.parse_args()

    config = load_config(args.config)

    jira_url = config['jira_url']
    username = config['username']
    api_token = config['api_token']
    jql = config['jql']
    fields = config['fields']
    output_file = config.get('output_file', 'issues.csv')
    include_links = config.get('include_issue_links', False)
    link_types = config.get('link_types', [])
    link_export_mode = config.get('link_export_mode', 'inline')
    relation_rules = config.get('relation_rules', [])

    auth = HTTPBasicAuth(username, api_token)

    print("Fetching issues from Jira...")
    issues = fetch_issues(jira_url, auth, jql, fields, include_links)

    print(f"Writing {len(issues)} issues to {output_file}...")
    write_issues_to_csv(
        issues, fields, output_file,
        include_links, link_types,
        link_export_mode, relation_rules,
        lambda *args, **kwargs: extract_links_flattened(*args, **kwargs, evaluate_relation=evaluate_relation),
        extract_issue_links
    )

    if include_links and link_export_mode == 'flattened':
        write_summary_csv(
            issues, fields, link_types, relation_rules,
            lambda *args, **kwargs: extract_links_flattened(*args, **kwargs, evaluate_relation=evaluate_relation),
            config
        )

    print("Done.")


if __name__ == '__main__':
    main()
