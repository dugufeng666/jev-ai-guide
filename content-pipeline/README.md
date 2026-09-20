# Jev AI Guide content pipeline

Source collection and draft generation for Jev AI Guide. This pipeline is for
English draft research only. It does not publish, deploy, translate, or modify
the website.

## Local installation

Tool checkout: `/Users/dugufeng/Desktop/github/seoscout`

Use the SEOScout checkout's `.venv/bin/python` to execute this directory's
`run.py`. The wrapper explicitly loads this directory's ignored `.env`, adds
SEOScout's virtualenv binaries such as `yt-dlp` to `PATH`, and selects
`generate-prompt.md` / `translate-prompt.md`.

If explicit LLM credentials are absent, the wrapper uses `OPENAI_API_KEY`
together with `OPENAI_BASE_URL`; it never sends that credential to the upstream
default endpoint. Default model for that fallback is `gpt-5.6-luna`; override
`LLM_MODEL` to an available model if needed.

```sh
cd /Users/dugufeng/Desktop/github/jev-ai-guide/content-pipeline
/Users/dugufeng/Desktop/github/seoscout/.venv/bin/python run.py search --keywords keywords.json
/Users/dugufeng/Desktop/github/seoscout/.venv/bin/python review-search.py
/Users/dugufeng/Desktop/github/seoscout/.venv/bin/python run.py collect --keywords keywords.json
/Users/dugufeng/Desktop/github/seoscout/.venv/bin/python supplement-official.py
/Users/dugufeng/Desktop/github/seoscout/.venv/bin/python run.py generate --keywords keywords.json
/Users/dugufeng/Desktop/github/seoscout/.venv/bin/python audit.py
```

For a per-run local proxy:

```sh
PIPELINE_PROXY_URL=http://127.0.0.1:7890 /Users/dugufeng/Desktop/github/seoscout/.venv/bin/python run.py search --keywords keywords.json
```

## Source and editorial gates

- Search results are candidates, not evidence. Review intent, date, and source
  type before generation.
- Missing Serper credentials means no Google results. Do not report web-search
  coverage from the number of YouTube results.
- `collect` skips existing material files; inspect files before resuming.
- `supplement-official.py` adds official TypeSafe, Cloudflare, and selected
  open-source project context directly into collected briefs.
- `generate-prompt.md` requires source-grounded drafts. Unsupported pages must
  return `INSUFFICIENT_EVIDENCE`, not generic filler.
- `draft_validation.py` enforces measurable draft gates before SEOScout saves a
  generated article.
- `audit.py` checks measurable format requirements, not factual accuracy. Every
  draft still needs source-based editorial review before publication.
- Do not translate until English content and site languages are confirmed.

## Never commit

The following stay local and are ignored:

- `.env`
- `output/`
- `digest/`
- raw transcript/cache/debug output

Credentials belong only in `.env` or environment variables.
