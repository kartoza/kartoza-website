#!/usr/bin/env python3
"""Shared ERPNext HTTP client utilities for the sync scripts in this directory.

Environment variables:
    ERPNEXT_URL: ERPNext instance URL (default: https://erp.kartoza.com)
    ERPNEXT_API_KEY: API key for authentication
    ERPNEXT_API_SECRET: API secret for authentication
"""

import os
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_env_file(path: Path) -> bool:
    """Load KEY=VALUE entries from a dotenv-like file into os.environ."""
    if not path.exists():
        return False

    try:
        lines = path.read_text().splitlines()
    except (IOError, OSError):
        return False

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()

        if key.startswith('export '):
            key = key[len('export '):].strip()

        if ((value.startswith('"') and value.endswith('"'))
                or (value.startswith("'") and value.endswith("'"))):
            value = value[1:-1]

        # Keep shell-exported values authoritative.
        if key and key not in os.environ:
            os.environ[key] = value

    return True


def _load_default_env_files() -> list[Path]:
    """Load common environment files used by this repository."""
    loaded_files: list[Path] = []
    candidates = [
        PROJECT_ROOT / '.env',
    ]
    for path in candidates:
        if _load_env_file(path):
            loaded_files.append(path)
        else:
            print(f"Error: env file not found: {path}")
    return loaded_files


def _normalize_erpnext_base_url(url: str) -> str:
    """Normalize ERPNext URL to a base URL without trailing /api."""
    normalized = url.strip().rstrip('/')
    if normalized.endswith('/api'):
        return normalized[:-4]
    return normalized


class ERPNextClient:
    """Small HTTP client wrapping a retrying requests.Session for ERPNext.

    Resolves the ERPNext base URL and API credentials from environment
    variables (loading `.env` first), and exposes `get`/`post` helpers
    that build full URLs and apply auth automatically.
    """

    def __init__(self, base_url: str | None = None, api_key: str | None = None,
                 api_secret: str | None = None):
        self.loaded_env_files = _load_default_env_files()

        raw_url = base_url or os.environ.get('ERPNEXT_URL', 'https://erp.kartoza.com')
        self.base_url = _normalize_erpnext_base_url(raw_url)

        self.api_key = api_key or os.environ.get('ERPNEXT_API_KEY') or ''
        self.api_secret = api_secret or os.environ.get('ERPNEXT_API_SECRET') or ''

        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()

        retry = Retry(
            total=5,
            connect=5,
            read=5,
            status=5,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(['GET']),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        session.mount('http://', adapter)

        session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'kartoza-website-sync/1.0',
        })

        if self.api_key and self.api_secret:
            session.headers.update({'Authorization': f'token {self.api_key}:{self.api_secret}'})

        return session

    @property
    def has_credentials(self) -> bool:
        return bool(self.api_key and self.api_secret)

    def resolve_url(self, path: str) -> str:
        """Return the absolute URL for a path (absolute URLs pass through unchanged)."""
        if path.startswith('http://') or path.startswith('https://'):
            return path
        return f"{self.base_url}{path if path.startswith('/') else '/' + path}"

    def get(self, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault('timeout', 30)
        url = self.resolve_url(path)
        return self.session.get(url, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault('timeout', 30)
        return self.session.post(self.resolve_url(path), **kwargs)