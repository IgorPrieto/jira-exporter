# extractors.py

def extract_field(data, field_path):
    keys = field_path.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, '')
        else:
            return ''
    return data

def extract_issue_links(issue, allowed_link_types):
    links = issue.get('fields', {}).get('issuelinks', [])
    related = []
    for link in links:
        link_type = link['type']['name']
        if allowed_link_types and link_type not in allowed_link_types:
            continue
        if 'outwardIssue' in link:
            related.append(f"{link_type} → {link['outwardIssue']['key']}")
        elif 'inwardIssue' in link:
            related.append(f"{link_type} ← {link['inwardIssue']['key']}")
    return ' | '.join(related)

def extract_links_flattened(issue, allowed_link_types, fields, relation_rules, issues_by_key, evaluate_relation):
    links = issue.get('fields', {}).get('issuelinks', [])
    rows = []
    for link in links:
        link_type = link['type']['name']
        if allowed_link_types and link_type not in allowed_link_types:
            continue
        base_data = {field: extract_field(issue['fields'], field) for field in fields}
        direction = 'outward' if 'outwardIssue' in link else 'inward'
        linked_key = link['outwardIssue']['key'] if direction == 'outward' else link['inwardIssue']['key']
        target_type = issues_by_key.get(linked_key, {}).get('fields', {}).get('issuetype', {}).get('name', '')
        status = evaluate_relation(
            relation_rules,
            base_data.get('issuetype.name', ''),
            base_data.get('status.name', ''),
            link_type,
            target_type
        ) if relation_rules else ''
        base_data.update({
            'link_type': link_type,
            'link_direction': direction,
            'linked_issue': linked_key,
            'relation_status': status
        })
        rows.append(base_data)
    return rows
