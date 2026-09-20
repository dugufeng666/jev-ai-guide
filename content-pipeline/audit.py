"""Report measurable template violations; never equate this with fact checking."""
import json
from pathlib import Path
import re
import argparse

root = Path(__file__).resolve().parent
keywords = json.loads((root / 'keywords.json').read_text())
project = keywords.get('topic_name', root.name).replace(' ', '_').replace('.', '_').replace('/', '_').lower()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--articles-dir', type=Path,
                    default=root / 'output' / project / 'articles/en')
args = parser.parse_args()
args.articles_dir = args.articles_dir.resolve()
mapping = {k.replace(' ', '-'): k for c in keywords['categories'] for k in c['keywords']}
results = []
for path in sorted(args.articles_dir.rglob('*.mdx')):
    text = path.read_text()
    match = re.match(r'export const metadata\s*=\s*(\{.*?\});?', text, re.S)
    issues = []
    try:
        if not match: raise ValueError('Missing metadata')
        meta = json.loads(match.group(1))
        body = text[match.end():]
    except (ValueError, json.JSONDecodeError):
        results.append({'file': str(path.relative_to(root)), 'issues': ['Invalid JSON-compatible metadata']})
        continue
    keyword = mapping[path.stem]
    title, description = meta.get('title', ''), meta.get('description', '')
    words = len(re.findall(r"\b[\w'-]+\b", body))
    headings = len(re.findall(r'^## ', body, re.M))
    tables = len(re.findall(r'^\|\s*:?-{3,}', body, re.M))
    mentions = text.lower().count(keyword)
    if not 50 <= len(title) <= 60: issues.append('Title length')
    if not 150 <= len(description) <= 155: issues.append('Description length')
    if keyword not in title.lower(): issues.append('Keyword missing from title')
    if keyword not in description.lower(): issues.append('Keyword missing from description')
    if mentions < 9: issues.append('Fewer than 9 keyword mentions')
    if not 4 <= headings <= 6: issues.append('H2 count')
    if not 3 <= tables <= 5: issues.append('Table count')
    if re.search(r'^# ', body, re.M): issues.append('Unexpected H1')
    if not 1400 <= words <= 1800: issues.append('Word count outside approximate target')
    if 'INSUFFICIENT_EVIDENCE' in text: issues.append('Evidence refusal saved as article')
    results.append({'file': str(path.relative_to(root)), 'title_chars': len(title),
                    'description_chars': len(description), 'words': words,
                    'keyword_mentions': mentions, 'h2_count': headings,
                    'table_count': tables, 'issues': issues,
                    'editorial_status': 'requires source review'})
print(json.dumps({'draft_count': len(results), 'articles': results}, indent=2))
