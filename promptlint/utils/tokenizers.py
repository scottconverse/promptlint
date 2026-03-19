"""tiktoken wrapper for token counting.

Provides cached encoding access and graceful fallback when tiktoken
is not installed.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any


_TIKTOKEN_AVAILABLE = True

try:
    import tiktoken
except ImportError:
    tiktoken = None  # type: ignore[assignment]
    _TIKTOKEN_AVAILABLE = False


@lru_cache(maxsize=8)
def get_encoding(name: str = "cl100k_base") -> Any:
    """Return a cached tiktoken encoding by name.

    Raises
    ------
    RuntimeError
        If tiktoken is not installed.
    ValueError
        If the encoding name is not recognized by tiktoken.
    """
    if not _TIKTOKEN_AVAILABLE:
        raise RuntimeError(
            "tiktoken is not installed. Install it with: pip install tiktoken"
        )
    return tiktoken.get_encoding(name)


def count_tokens(text: str, encoding: str = "cl100k_base") -> int:
    """Count the number of tokens in *text* using the specified encoding.

    Parameters
    ----------
    text:
        The string to tokenize.
    encoding:
        A tiktoken encoding name (default ``cl100k_base``).

    Returns
    -------
    int
        The token count.

    Raises
    ------
    RuntimeError
        If tiktoken is not installed.
    """
    enc = get_encoding(encoding)
    return len(enc.encode(text))
