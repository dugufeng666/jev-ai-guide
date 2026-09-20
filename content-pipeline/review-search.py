"""Apply first-pass exclusions to Jev AI search results."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATH = ROOT / 'output/jev_ai/out/search_results.json'

if not PATH.exists():
    raise SystemExit(f'Missing search results: {PATH}')

data = json.loads(PATH.read_text())

blocked_video_ids = {
    # FaZe Jev / gaming channel results; same word, different entity.
    '226Au8b7QZI',
    'USxNSsaeqjY',
    # Useful news topic but weak as source material for tutorial pages.
    'Spn-F83ZHH0',
}

blocked_title_fragments = (
    'modern warfare',
    'faze jev',
    'jev plays',
    'fake jev demos',
)

for entry in data.get('keywords', []):
    for item in entry.get('youtube', {}).get('items', []):
        title = item.get('title', '').lower()
        if item.get('video_id') in blocked_video_ids:
            item['selected'] = False
        elif any(fragment in title for fragment in blocked_title_fragments):
            item['selected'] = False

PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
selected = sum(
    item.get('selected', True)
    for entry in data.get('keywords', [])
    for item in entry.get('youtube', {}).get('items', [])
)
print('Selected videos:', selected)
