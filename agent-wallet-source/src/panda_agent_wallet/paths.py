# MIT License; see OPEN_SOURCE_LICENSE.md at the product root.
from __future__ import annotations

import os
import sys
from pathlib import Path


def config_dir() -> Path:
    """Return the per-user configuration directory without creating it."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
        return base / "PandaArb"
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/PandaArb"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "panda-arb"


def data_dir() -> Path:
    """Return the per-user mutable data directory without creating it."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
        return base / "PandaArb"
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/PandaArb"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "panda-arb"


def default_agent_env() -> Path:
    override = os.environ.get("PANDA_ARB_AGENT_ENV")
    if override:
        return Path(override).expanduser()
    modern = config_dir() / "agent.env"
    legacy = Path.home() / ".config/popdex/agent.env"
    return legacy if legacy.exists() and not modern.exists() else modern
