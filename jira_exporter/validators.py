def evaluate_relation(rule_set, issue_type, status, link_type, target_issue_type):
    for rule in rule_set:
        if rule['issue_type'] == issue_type and rule['status'] == status:
            if link_type in rule['allowed_link_types'] and target_issue_type in rule['allowed_target_issue_types']:
                return "Correct"
            else:
                return "Incorrect"
    return "No Rule Matched"
