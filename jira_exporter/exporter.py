import csv
import datetime
from .extractors import extract_field, extract_issue_links

def write_issues_to_csv(issues, fields, output_file, include_links, allowed_link_types, export_mode, relation_rules, extract_links_flattened, extract_issue_links):
    if include_links and export_mode == 'flattened':
        all_fields = fields + ['link_type', 'link_direction', 'linked_issue', 'relation_status']
    elif include_links:
        all_fields = fields + ['issue_links']
    else:
        all_fields = fields

    issues_by_key = {issue['key']: issue for issue in issues}

    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_fields)
        writer.writeheader()

        for issue in issues:
            if include_links and export_mode == 'flattened':
                rows = extract_links_flattened(issue, allowed_link_types, fields, relation_rules, issues_by_key)
                if rows:
                    for row in rows:
                        writer.writerow(row)
                else:
                    base_row = {field: extract_field(issue['fields'], field) for field in fields}
                    base_row.update({'link_type': '', 'link_direction': '', 'linked_issue': '', 'relation_status': ''})
                    writer.writerow(base_row)
            else:
                row = {field: extract_field(issue['fields'], field) for field in fields}
                if include_links:
                    row['issue_links'] = extract_issue_links(issue, allowed_link_types)
                writer.writerow(row)

def write_summary_csv(issues, fields, link_types, relation_rules, extract_links_flattened, config):
    summary_by_project = {}
    issues_by_key = {issue['key']: issue for issue in issues}
    all_rows = []

    for issue in issues:
        project_key = issue['key'].split('-')[0]
        if project_key not in summary_by_project:
            summary_by_project[project_key] = {'Correct': 0, 'Incorrect': 0, 'No Rule Matched': 0}

        rows = extract_links_flattened(issue, link_types, fields, relation_rules, issues_by_key)
        all_rows.extend(rows)
        for row in rows:
            status = row.get('relation_status', '')
            if status in summary_by_project[project_key]:
                summary_by_project[project_key][status] += 1

    if any(sum(counts.values()) > 0 for counts in summary_by_project.values()):
        base_summary_output_file = config.get('relation_summary_file', 'relation_summary.csv')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name_parts = base_summary_output_file.rsplit('.', 1)
        if len(name_parts) == 2:
            summary_output_file = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
        else:
            summary_output_file = f"{base_summary_output_file}_{timestamp}"

        print("\nRelation Summary by Project:")
        with open(summary_output_file, mode='w', newline='', encoding='utf-8') as summary_file:
            summary_writer = csv.writer(summary_file)
            summary_writer.writerow(['Project', 'Correct', 'Incorrect', 'No Rule Matched'])
            for project, counts in summary_by_project.items():
                print(f"Project {project}: Correct={counts['Correct']}, Incorrect={counts['Incorrect']}, No Rule Matched={counts['No Rule Matched']}")
                summary_writer.writerow([project, counts['Correct'], counts['Incorrect'], counts['No Rule Matched']])
        print(f"\nSummary saved to {summary_output_file}")
    else:
        print("\nNo relations evaluated. Summary file not created.")
