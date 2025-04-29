import requests
from requests.auth import HTTPBasicAuth

def fetch_issues(jira_url, auth, jql, fields, include_links):
    issues = []
    headers = {
        "Content-Type": "application/json"
    }
    next_page_token = None
    required_fields = list(set(field.split('.')[0] for field in fields))
    if include_links and 'issuelinks' not in required_fields:
        required_fields.append('issuelinks')

    while True:
        payload = {
            "jql": jql,
            "fields": required_fields
        }
        if next_page_token:
            payload["pageToken"] = next_page_token

        try:
            response = requests.post(
                f'{jira_url}/rest/api/3/search/jql',
                headers=headers,
                auth=auth,
                json=payload
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching issues: {e}")
            break

        data = response.json()
        issues.extend(data.get('issues', []))

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return issues
