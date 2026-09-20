"""Add official Jev/TypeSafe sources to collected briefs without overwriting."""
import json
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent

SOURCES = [
    (
        'https://docs.typesafe.ai/introduction.md',
        'TypeSafe AI introduction',
        ['guide', 'model', 'typesafe'],
    ),
    (
        'https://docs.typesafe.ai/models.md',
        'TypeSafe AI models and pricing',
        ['api', 'model', 'typesafe'],
    ),
    (
        'https://docs.typesafe.ai/primitives.md',
        'TypeSafe primitives',
        ['guide', 'model', 'api'],
    ),
    (
        'https://docs.typesafe.ai/model-jaggedness/jev-1.13.md',
        'Jev 1.13 jaggedness and limitations',
        ['guide', 'model', 'comparisons'],
    ),
    (
        'https://developers.cloudflare.com/ai/models/typesafe/jev/index.md',
        'Cloudflare AI model page for typesafe/jev',
        ['api', 'integrations'],
    ),
    (
        'https://github.com/browser-use/jev-ultrafast/raw/main/README.md',
        'Browser Use Jev Ultrafast README',
        ['agent', 'integrations', 'community'],
    ),
]


def project_dir(topic_name):
    return topic_name.replace(' ', '_').replace('.', '_').replace('/', '_').lower()


def main():
    keyword_data = json.loads((ROOT / 'keywords.json').read_text())
    topic = project_dir(keyword_data.get('topic_name', 'jev ai'))
    categories = keyword_data['categories']

    for url, title, category_names in SOURCES:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            content = response.text.strip()
            if len(content) < 500:
                raise ValueError('No substantive page content')
        except Exception as exc:
            print(title, type(exc).__name__, flush=True)
            continue

        for category in categories:
            if category['category'] not in category_names:
                continue
            for keyword in category['keywords']:
                path = (
                    ROOT / 'output' / topic / 'out' / 'collected' /
                    category['category'] / (keyword.replace(' ', '_') + '.json')
                )
                data = json.loads(path.read_text()) if path.exists() else {
                    'keyword': keyword,
                    'category': category['category'],
                    'collected_at': datetime.now().isoformat(),
                    'sources': {
                        'youtube': {'count': 0, 'videos': []},
                        'web': {'count': 0, 'pages': []},
                    },
                }
                pages = data['sources']['web']['pages']
                if not any(page['url'] == url for page in pages):
                    pages.append({
                        'type': 'web',
                        'title': title,
                        'url': url,
                        'content': content,
                        'collection_method': 'direct official markdown/html',
                        'retrieved_at': datetime.now().isoformat(),
                    })
                data['sources']['web']['count'] = len(pages)
                data['total_sources'] = len(pages) + len(data['sources']['youtube']['videos'])
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

        print('Official source collected:', title, len(content), 'characters', flush=True)


if __name__ == '__main__':
    main()
