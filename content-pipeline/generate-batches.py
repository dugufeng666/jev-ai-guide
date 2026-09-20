#!/usr/bin/env python3
"""Generate missing Jev AI articles one keyword at a time.

SEOScout saves articles only after its full generation and repair pass. This
runner isolates each keyword so a slow or unavailable LLM request cannot hold
the rest of the content queue hostage.
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SEOScout_PYTHON = Path("/Users/dugufeng/Desktop/github/seoscout/.venv/bin/python")


def slugify(value: str) -> str:
    return "".join(
        char if char.isalnum() or char == "-" else "-"
        for char in value.lower().replace(" ", "-")
    ).strip("-")


def article_path(project: str, category: str, keyword: str) -> Path:
    category_slug = category.lower().replace(" ", "-") if category else "general"
    return ROOT / "output" / project / "articles" / "en" / category_slug / f"{slugify(keyword)}.mdx"


def load_keywords(path: Path) -> list[tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = []
    for group in data.get("categories", []):
        category = group.get("category", "")
        entries.extend((keyword.strip(), category) for keyword in group.get("keywords", []))
    if not entries:
        entries = [(keyword.strip(), "") for keyword in data.get("keywords", [])]
    return entries


def build_subset(source: dict, entries: list[tuple[str, str]]) -> dict:
    grouped = {}
    for keyword, category in entries:
        grouped.setdefault(category, []).append(keyword)

    subset = {"topic_name": source.get("topic_name", "jev ai"), "categories": []}
    for category, keywords in grouped.items():
        subset["categories"].append({"category": category, "keywords": keywords})
    return subset


def run_one(subset_path: Path, env: dict, timeout: int) -> int:
    command = [
        str(SEOScout_PYTHON),
        "run.py",
        "generate",
        "--keywords",
        str(subset_path),
    ]
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        env=env,
        start_new_session=True,
    )
    try:
        return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"\nTimeout after {timeout}s; stopping this keyword.", flush=True)
        os.killpg(process.pid, signal.SIGINT)
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=10)
        return 124


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", default="keywords.json")
    parser.add_argument("--limit", type=int, default=0, help="Maximum articles to attempt")
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument(
        "--skip",
        action="append",
        default=[],
        help="Keyword to skip; may be supplied more than once",
    )
    args = parser.parse_args()

    keywords_path = (ROOT / args.keywords).resolve()
    source = json.loads(keywords_path.read_text(encoding="utf-8"))
    project = source.get("topic_name", "jev ai").replace(" ", "_").lower()
    entries = [
        (keyword, category)
        for keyword, category in load_keywords(keywords_path)
        if keyword not in set(args.skip)
        if not article_path(project, category, keyword).exists()
    ]
    if args.limit:
        entries = entries[: args.limit]

    print(f"Missing articles: {len(entries)}", flush=True)
    if not entries:
        return 0

    env = os.environ.copy()
    env.setdefault("GENERATE_BATCH_SIZE", "1")
    env.setdefault("GENERATE_CONCURRENT_LIMIT", "1")
    env.setdefault("LLM_RETRY_ATTEMPTS", "1")
    env.setdefault("LLM_TIMEOUT", "120")

    temp_parent = ROOT / ".tmp"
    temp_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="jev-ai-generate-", dir=temp_parent) as temp_dir:
        temp_root = Path(temp_dir)
        for index, entry in enumerate(entries, start=1):
            keyword, category = entry
            subset_path = temp_root / "keywords.json"
            subset_path.write_text(
                json.dumps(build_subset(source, [entry]), indent=2),
                encoding="utf-8",
            )
            print(f"\n[{index}/{len(entries)}] {keyword}", flush=True)
            run_one(subset_path, env, args.timeout)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
