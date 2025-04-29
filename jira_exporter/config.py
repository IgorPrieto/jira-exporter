import json

def load_config(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)

    required_keys = ['jira_url', 'username', 'api_token', 'jql', 'fields']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")

    if not isinstance(config['fields'], list):
        raise ValueError("The 'fields' configuration must be a list of field names")

    if 'link_export_mode' in config and config['link_export_mode'] not in ['inline', 'flattened']:
        raise ValueError("The 'link_export_mode' must be either 'inline' or 'flattened'")

    return config
