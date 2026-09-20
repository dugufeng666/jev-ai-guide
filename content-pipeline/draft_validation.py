"""Measured draft gates for this project's article template."""
import json
import re
from pathlib import Path

_keywords = json.loads((Path(__file__).parent / 'keywords.json').read_text())
_allowed_keywords = sorted(
    [keyword for group in _keywords['categories'] for keyword in group['keywords']],
    key=len, reverse=True,
)


def validate_draft(content):
    if 'INSUFFICIENT_EVIDENCE' in content:
        return False, 'Insufficient source evidence'
    match = re.match(r'^export const metadata\s*=\s*(\{.*?\});?', content, re.S)
    if not match:
        return False, 'Must begin with JS metadata export'
    try:
        meta = json.loads(match.group(1))
    except json.JSONDecodeError:
        return False, 'Metadata must be a JSON-compatible object'
    if not isinstance(meta, dict):
        return False, 'Metadata must be an object'
    issues = []
    for key, low, high in [('title', 50, 60), ('description', 150, 155)]:
        value = meta.get(key)
        if not isinstance(value, str) or not low <= len(value) <= high:
            actual = len(value) if isinstance(value, str) else 'missing'
            issues.append(f'{key} length {actual}; required {low}-{high} characters')
    body = content[match.end():]
    words = len(re.findall(r"\b[\w'-]+\b", body))
    headings = len(re.findall(r'^## ', body, re.M))
    tables = len(re.findall(r'^\|\s*:?-{3,}', body, re.M))
    if not 1400 <= words <= 1800:
        issues.append(f'{words} words; required 1400-1800 without padding')
    if not 4 <= headings <= 6:
        issues.append(f'{headings} H2s; required 4-6 including opening and FAQ')
    if not 3 <= tables <= 5:
        issues.append(f'{tables} tables; required 3-5 source-supported tables')
    if re.search(r'^# ', body, re.M):
        issues.append('Unexpected H1')
    if not body.lstrip().startswith('## '):
        issues.append('Body must start with an H2')
    if not all(meta.get(key) for key in ('category', 'date')):
        issues.append('Missing category/date')
    keyword = next((k for k in _allowed_keywords
                    if k in str(meta.get('title', '')).lower()), None)
    if not keyword:
        issues.append('Title missing a requested keyword')
    else:
        if keyword not in str(meta.get('description', '')).lower():
            issues.append('Description missing the main keyword')
        if content.lower().count(keyword) < 9:
            issues.append('Main keyword must occur at least nine times naturally')
        opening = ' '.join(re.findall(r"\b[\w'-]+\b", body.lower())[:120])
        if opening.count(keyword) < 2:
            issues.append('Main keyword must occur twice within the opening 120 words')
    return not issues, '; '.join(issues)
