"""Token-count caching for promptlint.

Uses SHA256-based cache keys so unchanged files skip re-tokenization.
Cache is stored as a JSON file in ``.promptlint-cache/``.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_CACHE_VERSION = 1
_CACHE_DIR_NAME = ".promptlint-cache"
_CACHE_FILE_NAME = "cache.json"


def _cache_key(content: str, encoding: str) -> str:
    """Compute a SHA256 cache key from file content + encoding name."""
    raw = (content + encoding).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _cache_file(cache_dir: Path) -> Path:
    """Return the path to the cache JSON file."""
    return cache_dir / _CACHE_FILE_NAME


def _load_cache(cache_dir: Path) -> dict[str, Any]:
    """Load the cache JSON, returning a valid structure or fresh dict."""
    cf = _cache_file(cache_dir)
    if not cf.is_file():
        return {"version": _CACHE_VERSION, "entries": {}}

    try:
        data = json.loads(cf.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"version": _CACHE_VERSION, "entries": {}}

    if not isinstance(data, dict) or data.get("version") != _CACHE_VERSION:
        return {"version": _CACHE_VERSION, "entries": {}}

    return data


def _save_cache(cache_dir: Path, data: dict[str, Any]) -> None:
    """Write the cache dict to disk, creating the directory if needed."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cf = _cache_file(cache_dir)
    cf.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _default_cache_dir(path: Path) -> Path:
    """Resolve the default cache directory relative to the target path."""
    base = path.resolve()
    if base.is_file():
        base = base.parent
    return base / _CACHE_DIR_NAME


def get_cached(
    path: Path,
    content: str,
    encoding: str,
    cache_dir: Path | None = None,
) -> int | None:
    """Look up a cached token count for the given file content and encoding.

    Parameters
    ----------
    path:
        The prompt file path (used for metadata only).
    content:
        The raw file content.
    encoding:
        The tiktoken encoding name.
    cache_dir:
        Optional explicit cache directory.  Defaults to
        ``.promptlint-cache/`` next to *path*.

    Returns
    -------
    int | None
        The cached token count, or ``None`` on cache miss.
    """
    if cache_dir is None:
        cache_dir = _default_cache_dir(path)

    data = _load_cache(cache_dir)
    key = _cache_key(content, encoding)
    entry = data.get("entries", {}).get(key)
    if entry is None:
        return None

    return entry.get("token_count")


def set_cached(
    path: Path,
    content: str,
    encoding: str,
    token_count: int,
    cache_dir: Path | None = None,
) -> None:
    """Store a token count in the cache.

    Parameters
    ----------
    path:
        The prompt file path (stored as metadata).
    content:
        The raw file content.
    encoding:
        The tiktoken encoding name.
    token_count:
        The computed token count.
    cache_dir:
        Optional explicit cache directory.
    """
    if cache_dir is None:
        cache_dir = _default_cache_dir(path)

    data = _load_cache(cache_dir)
    key = _cache_key(content, encoding)

    data.setdefault("entries", {})[key] = {
        "path": str(path),
        "token_count": token_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    _save_cache(cache_dir, data)


def clear_cache(cache_dir: Path) -> None:
    """Remove the entire cache directory and its contents.

    Parameters
    ----------
    cache_dir:
        The cache directory to remove.  No-op if it does not exist.
    """
    if cache_dir.is_dir():
        shutil.rmtree(cache_dir)
