"""Built-in model profiles for context-aware linting.

Each profile maps a model name to its context window size, tokenizer
encoding, and max output token limit.
"""

from __future__ import annotations

from typing import Optional

from promptlint.models import ModelProfile


BUILTIN_PROFILES: dict[str, ModelProfile] = {
    "gpt-4": ModelProfile(
        name="gpt-4",
        context_window=8_192,
        tokenizer_encoding="cl100k_base",
        max_output_tokens=4_096,
    ),
    "gpt-4-turbo": ModelProfile(
        name="gpt-4-turbo",
        context_window=128_000,
        tokenizer_encoding="cl100k_base",
        max_output_tokens=4_096,
    ),
    "gpt-4o": ModelProfile(
        name="gpt-4o",
        context_window=128_000,
        tokenizer_encoding="o200k_base",
        max_output_tokens=16_384,
    ),
    "claude-3-haiku": ModelProfile(
        name="claude-3-haiku",
        context_window=200_000,
        tokenizer_encoding="cl100k_base",
        max_output_tokens=4_096,
        approximate_tokenizer=True,
    ),
    "claude-3-sonnet": ModelProfile(
        name="claude-3-sonnet",
        context_window=200_000,
        tokenizer_encoding="cl100k_base",
        max_output_tokens=8_192,
        approximate_tokenizer=True,
    ),
    "claude-3-opus": ModelProfile(
        name="claude-3-opus",
        context_window=200_000,
        tokenizer_encoding="cl100k_base",
        max_output_tokens=4_096,
        approximate_tokenizer=True,
    ),
    "claude-4-sonnet": ModelProfile(
        name="claude-4-sonnet",
        context_window=200_000,
        tokenizer_encoding="cl100k_base",
        max_output_tokens=64_000,
        approximate_tokenizer=True,
    ),
    "gemini-1.5-pro": ModelProfile(
        name="gemini-1.5-pro",
        context_window=1_000_000,
        tokenizer_encoding="cl100k_base",
        max_output_tokens=8_192,
        approximate_tokenizer=True,
    ),
    "gemini-2.0-flash": ModelProfile(
        name="gemini-2.0-flash",
        context_window=1_000_000,
        tokenizer_encoding="cl100k_base",
        max_output_tokens=8_192,
        approximate_tokenizer=True,
    ),
}


def get_profile(name: str) -> Optional[ModelProfile]:
    """Look up a built-in model profile by name.

    Parameters
    ----------
    name:
        The model profile name (e.g. ``"gpt-4o"``, ``"claude-3-sonnet"``).

    Returns
    -------
    ModelProfile | None
        The matching profile, or ``None`` if no built-in profile exists.
    """
    return BUILTIN_PROFILES.get(name)
