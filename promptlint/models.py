"""Core data models for promptlint.

All models use Pydantic v2 syntax with model_config and Field defaults.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Severity levels for lint violations."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class PromptFormat(str, Enum):
    """Supported prompt file formats."""

    TEXT = "text"       # .txt
    MARKDOWN = "md"     # .md
    YAML = "yaml"       # .yaml / .yml
    JSON = "json"       # .json


class Message(BaseModel):
    """Represents a single turn within a prompt."""

    model_config = {"frozen": False}

    role: str = Field(..., description="One of system, user, assistant")
    content: str = Field(..., description="The text content of the message")
    line_start: int = Field(
        ..., description="Line number where this message begins in the source file"
    )
    token_count: Optional[int] = Field(
        default=None,
        description="Token count, populated by the engine before rule evaluation",
    )


class PromptFile(BaseModel):
    """Represents a single parsed prompt file loaded by the parser."""

    model_config = {"frozen": False}

    path: Path = Field(..., description="Absolute path to the source file")
    format: PromptFormat = Field(..., description="Detected format enum")
    raw_content: str = Field(..., description="Original unmodified file content")
    messages: list[Message] = Field(
        default_factory=list, description="Parsed list of messages"
    )
    variables: dict[str, str] = Field(
        default_factory=dict,
        description="Extracted template variables (e.g. {{variable}})",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional front-matter or top-level YAML/JSON metadata",
    )
    total_tokens: Optional[int] = Field(
        default=None,
        description="Total token count across all messages, populated by engine",
    )


class PipelineStage(BaseModel):
    """Represents one stage in a prompt pipeline."""

    model_config = {"frozen": False}

    name: str = Field(..., description="Stage name (e.g. prior-art-search)")
    prompt_file: PromptFile = Field(
        ..., description="The parsed prompt file for this stage"
    )
    depends_on: list[str] = Field(
        default_factory=list,
        description="Names of stages whose output this stage consumes",
    )
    expected_output_tokens: Optional[int] = Field(
        default=None,
        description="Estimated output token count (for context growth analysis)",
    )
    persona: Optional[str] = Field(
        default=None, description="Declared persona/role for this stage"
    )


class PromptPipeline(BaseModel):
    """Represents an ordered set of prompt files that form a multi-stage pipeline."""

    model_config = {"frozen": False}

    name: str = Field(..., description="Pipeline name")
    stages: list[PipelineStage] = Field(
        default_factory=list, description="Ordered list of stages"
    )
    manifest_path: Path = Field(
        ..., description="Path to the .promptlint-pipeline.yaml manifest"
    )
    total_tokens: Optional[int] = Field(
        default=None, description="Sum of all stage token counts"
    )
    cumulative_tokens: Optional[list[int]] = Field(
        default=None,
        description="Running total at each stage (for context window analysis)",
    )


class LintViolation(BaseModel):
    """Represents a single rule violation produced by the engine."""

    model_config = {"frozen": False}

    rule_id: str = Field(..., description="Rule identifier, e.g. PL001")
    severity: Severity = Field(..., description="Violation severity level")
    message: str = Field(
        ..., description="Human-readable description of the violation"
    )
    suggestion: Optional[str] = Field(
        default=None, description="Optional actionable fix suggestion"
    )
    path: Path = Field(
        ..., description="Source file where the violation was found"
    )
    line: Optional[int] = Field(
        default=None, description="Line number of the violation, if applicable"
    )
    rule_name: str = Field(
        ...,
        description="Short slug name of the rule, e.g. token-budget-exceeded",
    )
    fixable: bool = Field(
        default=False,
        description="Whether this violation can be auto-fixed",
    )


class ModelProfile(BaseModel):
    """Built-in model configuration for context-aware linting."""

    model_config = {"frozen": True}

    name: str = Field(..., description="Model identifier")
    context_window: int = Field(
        ..., description="Maximum context window in tokens"
    )
    tokenizer_encoding: str = Field(
        ..., description="tiktoken encoding to use"
    )
    max_output_tokens: int = Field(
        ..., description="Typical max output tokens"
    )
    approximate_tokenizer: bool = Field(
        default=False,
        description="True if the tokenizer is an approximation (provider does not publish native tokenizer)",
    )


class LintConfig(BaseModel):
    """Merged configuration from file + CLI flags + defaults."""

    model_config = {"frozen": False}

    model: Optional[str] = Field(
        default=None,
        description="Model profile name (auto-sets context window + tokenizer)",
    )
    tokenizer_encoding: str = Field(
        default="cl100k_base", description="tiktoken encoding name"
    )
    token_warn_threshold: int = Field(
        default=2048, description="PL001 warning threshold"
    )
    token_error_threshold: int = Field(
        default=4096, description="PL002 error threshold"
    )
    system_prompt_threshold: int = Field(
        default=1024, description="PL014 system prompt threshold"
    )
    stop_word_ratio: float = Field(
        default=0.60, description="PL003 stop-word ratio threshold"
    )
    max_line_length: int = Field(
        default=500, description="PL024 character limit"
    )
    repetition_threshold: int = Field(
        default=3, description="PL023 occurrence count"
    )
    rule_overrides: dict[str, str] = Field(
        default_factory=dict, description="Per-rule severity overrides"
    )
    ignored_rules: list[str] = Field(
        default_factory=list, description="Globally ignored rule IDs"
    )
    exclude_patterns: list[str] = Field(
        default_factory=list, description="Glob patterns for excluded files"
    )
    plugin_dirs: list[Path] = Field(
        default_factory=list,
        description="Directories containing custom rule plugins",
    )
    context_window: Optional[int] = Field(
        default=None,
        description="Model context window (auto-set by model profile, or manual)",
    )
