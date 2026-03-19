"""File parser for promptlint.

Detects format by file extension, parses each format into a
``PromptFile``, and extracts template variables.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from promptlint.models import (
    Message,
    PipelineStage,
    PromptFile,
    PromptFormat,
    PromptPipeline,
)

# ---------------------------------------------------------------------------
# Variable extraction
# ---------------------------------------------------------------------------

# Patterns for template variables, ordered by specificity
_JINJA_VAR_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")       # {{var}}
_FSTRING_VAR_RE = re.compile(r"(?<!\{)\{(\w+)\}(?!\})")   # {var}  (not {{var}})
_XML_VAR_RE = re.compile(r"<(\w+)>(?!</)")                 # <var>  (not closing tags)

# Combined pattern for detecting any variable style
_ALL_VAR_RE = re.compile(
    r"\{\{\s*(\w+)\s*\}\}"       # {{var}}
    r"|(?<!\{)\{(\w+)\}(?!\})"   # {var}
    r"|<(\w+)>"                   # <var>
)

# Common XML/HTML tags to exclude from variable detection
_EXCLUDED_XML_TAGS = frozenset({
    "br", "hr", "p", "div", "span", "a", "b", "i", "u", "em", "strong",
    "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "table", "tr",
    "td", "th", "thead", "tbody", "img", "code", "pre", "blockquote",
    "html", "head", "body", "meta", "link", "script", "style", "section",
    "article", "nav", "footer", "header", "main", "aside", "form", "input",
    "button", "label", "select", "option", "textarea",
})

_FORMAT_MAP: dict[str, PromptFormat] = {
    ".txt": PromptFormat.TEXT,
    ".md": PromptFormat.MARKDOWN,
    ".yaml": PromptFormat.YAML,
    ".yml": PromptFormat.YAML,
    ".json": PromptFormat.JSON,
}


def _detect_format(path: Path) -> PromptFormat:
    """Determine prompt format from the file extension."""
    ext = path.suffix.lower()
    fmt = _FORMAT_MAP.get(ext)
    if fmt is None:
        raise ValueError(
            f"Unsupported file extension '{ext}' for {path}. "
            f"Supported: {', '.join(_FORMAT_MAP)}"
        )
    return fmt


def _extract_variables(text: str) -> dict[str, str]:
    """Detect ``{{var}}``, ``{var}``, and ``<var>`` patterns in *text*.

    Returns a dict mapping variable name to the syntax style used
    (``jinja``, ``fstring``, or ``xml``).
    """
    variables: dict[str, str] = {}

    for match in _JINJA_VAR_RE.finditer(text):
        variables[match.group(1)] = "jinja"

    for match in _FSTRING_VAR_RE.finditer(text):
        name = match.group(1)
        if name not in variables:
            variables[name] = "fstring"

    for match in _XML_VAR_RE.finditer(text):
        name = match.group(1)
        if name.lower() not in _EXCLUDED_XML_TAGS and name not in variables:
            variables[name] = "xml"

    return variables


# ---------------------------------------------------------------------------
# Sub-parsers
# ---------------------------------------------------------------------------

def _parse_text(path: Path, content: str) -> PromptFile:
    """Parse a plain text file as a single user message."""
    variables = _extract_variables(content)
    return PromptFile(
        path=path.resolve(),
        format=PromptFormat.TEXT,
        raw_content=content,
        messages=[
            Message(role="user", content=content, line_start=1),
        ],
        variables=variables,
    )


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_markdown(path: Path, content: str) -> PromptFile:
    """Parse a Markdown file, extracting optional YAML frontmatter."""
    metadata: dict[str, Any] = {}
    body = content
    body_start_line = 1

    fm_match = _FRONTMATTER_RE.match(content)
    if fm_match:
        fm_text = fm_match.group(1)
        parsed = yaml.safe_load(fm_text)
        if isinstance(parsed, dict):
            metadata = parsed
        body = content[fm_match.end():]
        # Count lines consumed by frontmatter
        body_start_line = content[: fm_match.end()].count("\n") + 1

    variables = _extract_variables(body)
    return PromptFile(
        path=path.resolve(),
        format=PromptFormat.MARKDOWN,
        raw_content=content,
        messages=[
            Message(role="user", content=body, line_start=body_start_line),
        ],
        variables=variables,
        metadata=metadata,
    )


def _parse_yaml(path: Path, content: str) -> PromptFile:
    """Parse a YAML prompt file expecting a ``messages`` list."""
    data = yaml.safe_load(content)
    if not isinstance(data, dict):
        raise ValueError(f"YAML prompt file {path} must contain a mapping at the top level")

    messages_raw = data.get("messages")
    if not isinstance(messages_raw, list):
        raise ValueError(
            f"YAML prompt file {path} must contain a 'messages' list"
        )

    # Metadata is everything except "messages"
    metadata = {k: v for k, v in data.items() if k != "messages"}

    messages: list[Message] = []
    # Approximate line numbers by scanning content for role keys
    content_lines = content.split("\n")
    role_line_indices: list[int] = []
    for idx, line in enumerate(content_lines, start=1):
        stripped = line.strip()
        if stripped.startswith("- role:") or stripped.startswith("role:"):
            role_line_indices.append(idx)

    for i, msg_raw in enumerate(messages_raw):
        if not isinstance(msg_raw, dict):
            raise ValueError(
                f"Each message in {path} must be a mapping with 'role' and 'content'"
            )
        role = str(msg_raw.get("role", "user"))
        msg_content = str(msg_raw.get("content", ""))
        line_start = role_line_indices[i] if i < len(role_line_indices) else 1
        messages.append(Message(role=role, content=msg_content, line_start=line_start))

    all_content = " ".join(m.content for m in messages)
    variables = _extract_variables(all_content)

    return PromptFile(
        path=path.resolve(),
        format=PromptFormat.YAML,
        raw_content=content,
        messages=messages,
        variables=variables,
        metadata=metadata,
    )


def _parse_json(path: Path, content: str) -> PromptFile:
    """Parse a JSON prompt file.

    Supports two layouts:
      - ``{"messages": [...]}`` — OpenAI chat format
      - ``{"prompt": "..."}`` — single prompt string
    """
    data = json.loads(content)
    metadata: dict[str, Any] = {}

    if isinstance(data, dict):
        if "messages" in data:
            messages_raw = data["messages"]
            if not isinstance(messages_raw, list):
                raise ValueError(
                    f"JSON prompt file {path}: 'messages' must be an array"
                )
            metadata = {k: v for k, v in data.items() if k != "messages"}
            messages: list[Message] = []
            for i, msg_raw in enumerate(messages_raw):
                if not isinstance(msg_raw, dict):
                    raise ValueError(
                        f"Each message in {path} must be an object with 'role' and 'content'"
                    )
                role = str(msg_raw.get("role", "user"))
                msg_content = str(msg_raw.get("content", ""))
                messages.append(Message(role=role, content=msg_content, line_start=i + 1))

            all_content = " ".join(m.content for m in messages)
            variables = _extract_variables(all_content)
            return PromptFile(
                path=path.resolve(),
                format=PromptFormat.JSON,
                raw_content=content,
                messages=messages,
                variables=variables,
                metadata=metadata,
            )

        elif "prompt" in data:
            prompt_text = str(data["prompt"])
            metadata = {k: v for k, v in data.items() if k != "prompt"}
            variables = _extract_variables(prompt_text)
            return PromptFile(
                path=path.resolve(),
                format=PromptFormat.JSON,
                raw_content=content,
                messages=[Message(role="user", content=prompt_text, line_start=1)],
                variables=variables,
                metadata=metadata,
            )

    raise ValueError(
        f"JSON prompt file {path} must contain a 'messages' array or 'prompt' string"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_SUB_PARSERS = {
    PromptFormat.TEXT: _parse_text,
    PromptFormat.MARKDOWN: _parse_markdown,
    PromptFormat.YAML: _parse_yaml,
    PromptFormat.JSON: _parse_json,
}


def parse_file(path: Path) -> PromptFile:
    """Parse a prompt file at *path*, auto-detecting format by extension.

    Parameters
    ----------
    path:
        Path to the prompt file.

    Returns
    -------
    PromptFile
        The parsed prompt.

    Raises
    ------
    ValueError
        If the format is unsupported or the file content is malformed.
    FileNotFoundError
        If the file does not exist.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {path}")

    fmt = _detect_format(path)
    content = path.read_text(encoding="utf-8")
    parser_fn = _SUB_PARSERS[fmt]
    return parser_fn(path, content)


def parse_stdin(content: str, format: str) -> PromptFile:
    """Parse prompt content read from stdin.

    Parameters
    ----------
    content:
        The raw text read from stdin.
    format:
        One of ``text``, ``md``, ``yaml``, ``json``.

    Returns
    -------
    PromptFile
        The parsed prompt with ``path`` set to ``Path("-")``.
    """
    fmt_map = {
        "text": PromptFormat.TEXT,
        "md": PromptFormat.MARKDOWN,
        "yaml": PromptFormat.YAML,
        "json": PromptFormat.JSON,
    }
    fmt = fmt_map.get(format)
    if fmt is None:
        raise ValueError(
            f"Unsupported input format '{format}'. "
            f"Supported: {', '.join(fmt_map)}"
        )

    stdin_path = Path("-")
    parser_fn = _SUB_PARSERS[fmt]
    return parser_fn(stdin_path, content)


def parse_pipeline_manifest(path: Path) -> PromptPipeline:
    """Parse a ``.promptlint-pipeline.yaml`` manifest and all referenced
    prompt files.

    Parameters
    ----------
    path:
        Path to the pipeline manifest YAML.

    Returns
    -------
    PromptPipeline
        A pipeline with all stages parsed.

    Raises
    ------
    ValueError
        If the manifest is malformed or a referenced prompt file is
        missing.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Pipeline manifest not found: {path}")

    content = path.read_text(encoding="utf-8")
    data = yaml.safe_load(content)
    if not isinstance(data, dict):
        raise ValueError(f"Pipeline manifest {path} must be a YAML mapping")

    name = str(data.get("name", path.stem))
    manifest_dir = path.parent

    stages_raw = data.get("stages")
    if not isinstance(stages_raw, list):
        raise ValueError(f"Pipeline manifest {path} must contain a 'stages' list")

    stages: list[PipelineStage] = []
    for stage_raw in stages_raw:
        if not isinstance(stage_raw, dict):
            raise ValueError("Each pipeline stage must be a mapping")

        stage_name = str(stage_raw.get("name", "unnamed"))
        file_rel = stage_raw.get("file")
        if not file_rel:
            raise ValueError(f"Pipeline stage '{stage_name}' is missing 'file' key")

        prompt_path = manifest_dir / file_rel
        prompt_file = parse_file(prompt_path)

        depends_on = stage_raw.get("depends_on", [])
        if not isinstance(depends_on, list):
            depends_on = [depends_on]

        stages.append(
            PipelineStage(
                name=stage_name,
                prompt_file=prompt_file,
                depends_on=[str(d) for d in depends_on],
                expected_output_tokens=stage_raw.get("expected_output_tokens"),
                persona=stage_raw.get("persona"),
            )
        )

    return PromptPipeline(
        name=name,
        stages=stages,
        manifest_path=path.resolve(),
    )
