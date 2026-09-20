"""Run the installed seoscout with this project's explicit configuration."""
import os
from pathlib import Path
import socket
import sys

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
load_dotenv(ROOT / '.env')
os.environ['PATH'] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get('PATH', '')

# Local DNS sometimes fails while direct IP connectivity is still available.
# Keep this fallback narrowly scoped to the external services used by this
# pipeline so seoscout can continue without changing system DNS settings.
_PINNED_HOSTS = {
    'google.serper.dev': ['34.111.29.75'],
    'r.jina.ai': ['104.26.10.242', '104.26.11.242', '172.67.70.54'],
    'rehdasu.cn': ['104.26.10.35', '104.26.11.35', '172.67.74.111'],
}
_ORIGINAL_GETADDRINFO = socket.getaddrinfo


def _getaddrinfo_with_pipeline_fallback(host, port, family=0, type=0, proto=0, flags=0):
    try:
        return _ORIGINAL_GETADDRINFO(host, port, family, type, proto, flags)
    except socket.gaierror:
        ips = _PINNED_HOSTS.get(str(host).lower())
        if not ips:
            raise
        return [
            (socket.AF_INET, type or socket.SOCK_STREAM, proto, '', (ip, port))
            for ip in ips
        ]


socket.getaddrinfo = _getaddrinfo_with_pipeline_fallback

# Preserve the configured credential/endpoint pairing; never use upstream's
# default third-party endpoint with an unrelated provider's credential.
if not os.environ.get('LLM_API_KEY'):
    if os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_BASE_URL'):
        os.environ['LLM_API_KEY'] = os.environ['OPENAI_API_KEY']
        os.environ['LLM_API_BASE_URL'] = os.environ['OPENAI_BASE_URL']
        os.environ['LLM_MODEL'] = os.environ.get('LLM_MODEL') or 'gpt-5.6-luna'

if len(sys.argv) > 1 and sys.argv[1] in ('generate', 'translate', 'run'):
    if not all(os.environ.get(k) for k in ('LLM_API_KEY', 'LLM_API_BASE_URL', 'LLM_MODEL')):
        raise SystemExit('Configure LLM_API_KEY, LLM_API_BASE_URL and LLM_MODEL in .env.')
    if sys.argv[1] in ('generate', 'run') and '--prompt' not in sys.argv:
        sys.argv.extend(['--prompt', str(ROOT / 'generate-prompt.md')])
    if sys.argv[1] == 'translate' and '--prompt' not in sys.argv:
        sys.argv.extend(['--prompt', str(ROOT / 'translate-prompt.md')])

from seoscout.cli import main

if len(sys.argv) > 1 and sys.argv[1] in ('generate', 'run'):
    import seoscout.generate as _generate
    from draft_validation import validate_draft

    _generate.validate_markdown = validate_draft

# Optional per-run transport override, useful when the tunnel rejects the
# current client IP. Credentials and the configured tunnel remain untouched.
if os.environ.get('PIPELINE_PROXY_URL'):
    from urllib.parse import urlsplit
    from seoscout.core.config import Config

    _pipeline_proxy = os.environ['PIPELINE_PROXY_URL']
    if urlsplit(_pipeline_proxy).scheme not in ('http', 'https', 'socks5', 'socks5h'):
        raise SystemExit('PIPELINE_PROXY_URL must be a supported proxy URL.')
    Config.get_proxy_url_for_stage = classmethod(lambda cls, stage: _pipeline_proxy)
    Config.get_proxy_url = classmethod(lambda cls: _pipeline_proxy)

if __name__ == '__main__':
    main()
