"""Profile-aware filesystem paths for Hermes-Jev.

Hermes named profiles are selected by setting ``HERMES_HOME`` before startup,
and newer multiplexed hosts can additionally use a context-local Hermes-home
override. Prefer Hermes' own resolver when importable; fall back to environment
and finally ``~/.hermes`` so the package remains usable in standalone tests.
"""

from __future__ import annotations

import os
from pathlib import Path


def hermes_home() -> Path:
    try:
        from hermes_constants import get_hermes_home  # type: ignore
        value = get_hermes_home()
        if value:
            return Path(value).expanduser()
    except Exception:
        pass
    explicit = str(os.getenv("HERMES_HOME") or "").strip()
    return Path(explicit).expanduser() if explicit else Path.home() / ".hermes"


def default_hermes_root() -> Path:
    try:
        from hermes_constants import get_default_hermes_root  # type: ignore
        value = get_default_hermes_root()
        if value:
            return Path(value).expanduser()
    except Exception:
        pass
    home = hermes_home()
    if home.parent.name == "profiles":
        return home.parent.parent
    return Path.home() / ".hermes"


def infer_profile_home_from_path(path: Path | None = None) -> Path | None:
    """Infer ``<root>/profiles/<name>`` when *path* is inside a named profile."""
    candidate = (path or Path.cwd()).expanduser().resolve(strict=False)
    parts = candidate.parts
    for index in range(len(parts) - 2):
        if parts[index] == "profiles" and index + 1 < len(parts):
            return Path(*parts[: index + 2])
    return None


def report_home(path: Path | None = None) -> Path:
    """Best home for a standalone report command.

    Running a plugin script directly does not inherit the wrapper's HERMES_HOME.
    If the script is launched from inside a named profile plugin directory, use
    that profile rather than silently falling back to the global default home.
    """
    explicit = str(os.getenv("HERMES_HOME") or "").strip()
    if explicit:
        return Path(explicit).expanduser()
    inferred = infer_profile_home_from_path(path)
    return inferred if inferred is not None else hermes_home()
