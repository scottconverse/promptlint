"""Plugin discovery and loading for custom promptlint rules.

Scans configured plugin directories for Python files, imports them, and
discovers any classes that subclass ``BaseRule`` or ``BasePipelineRule``.
Plugin rule IDs must start with ``PLX`` to avoid collisions with built-in
rules.
"""

from __future__ import annotations

import importlib.util
import logging
import sys
from pathlib import Path
from typing import Union

from promptlint.rules.base import BasePipelineRule, BaseRule

logger = logging.getLogger(__name__)


def _is_rule_subclass(obj: object) -> bool:
    """Return True if *obj* is a concrete subclass of BaseRule or BasePipelineRule."""
    try:
        return (
            isinstance(obj, type)
            and (issubclass(obj, (BaseRule, BasePipelineRule)))
            and obj not in (BaseRule, BasePipelineRule)
            and not getattr(obj, "__abstractmethods__", None)
        )
    except TypeError:
        return False


def _validate_plugin_rule_id(rule_cls: type) -> bool:
    """Ensure plugin rule IDs start with PLX."""
    rule_id: str = getattr(rule_cls, "rule_id", "")
    if not rule_id.startswith("PLX"):
        logger.warning(
            "Plugin rule %s has rule_id '%s' which does not start with 'PLX'. "
            "Skipping.",
            rule_cls.__name__,
            rule_id,
        )
        return False
    return True


def load_plugins_from_directory(
    directory: Path,
) -> list[Union[BaseRule, BasePipelineRule]]:
    """Scan a single directory for plugin rule classes and return instances.

    Parameters
    ----------
    directory:
        Path to a directory containing ``.py`` files with rule classes.

    Returns
    -------
    list:
        Instantiated rule objects discovered in the directory.
    """
    instances: list[Union[BaseRule, BasePipelineRule]] = []

    if not directory.is_dir():
        logger.warning("Plugin directory does not exist: %s", directory)
        return instances

    for py_file in sorted(directory.glob("*.py")):
        if py_file.name.startswith("_"):
            continue

        module_name = f"promptlint_plugin_{py_file.stem}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            if spec is None or spec.loader is None:
                logger.warning("Could not load module spec for %s", py_file)
                continue

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)  # type: ignore[union-attr]

            for attr_name in dir(module):
                obj = getattr(module, attr_name)
                if _is_rule_subclass(obj) and _validate_plugin_rule_id(obj):
                    try:
                        instance = obj()
                        instances.append(instance)
                        logger.debug(
                            "Loaded plugin rule %s (%s) from %s",
                            instance.rule_id,
                            instance.name,
                            py_file,
                        )
                    except Exception:
                        logger.exception(
                            "Failed to instantiate plugin rule %s from %s",
                            attr_name,
                            py_file,
                        )
        except Exception:
            logger.exception("Failed to import plugin file %s", py_file)
        finally:
            # Clean up to allow re-import if needed
            sys.modules.pop(module_name, None)

    return instances


def load_plugins(
    plugin_dirs: list[Path],
) -> list[Union[BaseRule, BasePipelineRule]]:
    """Load plugin rules from all configured directories.

    Parameters
    ----------
    plugin_dirs:
        List of directory paths to scan for plugin ``.py`` files.

    Returns
    -------
    list:
        All discovered and validated plugin rule instances.
    """
    all_plugins: list[Union[BaseRule, BasePipelineRule]] = []
    seen_ids: set[str] = set()

    for directory in plugin_dirs:
        plugins = load_plugins_from_directory(directory)
        for plugin in plugins:
            if plugin.rule_id in seen_ids:
                logger.warning(
                    "Duplicate plugin rule_id '%s' from %s. Skipping.",
                    plugin.rule_id,
                    directory,
                )
                continue
            seen_ids.add(plugin.rule_id)
            all_plugins.append(plugin)

    return all_plugins
