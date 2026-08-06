#!/usr/bin/env python3
"""Validate bridge repository metadata and package ownership."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "pylontech_h3x_bridge"
REPOSITORY_URL = "https://github.com/shuffleznl/h3x-bridge"


def main() -> None:
    """Check URLs, domain stability, and dashboard separation."""
    manifest = json.loads((COMPONENT / "manifest.json").read_text(encoding="utf-8"))
    if manifest["domain"] != "pylontech_h3x_bridge":
        raise AssertionError("Home Assistant domain must remain pylontech_h3x_bridge")
    if manifest["documentation"] != REPOSITORY_URL:
        raise AssertionError("manifest documentation points to the wrong repository")
    if manifest["issue_tracker"] != f"{REPOSITORY_URL}/issues":
        raise AssertionError("manifest issue tracker points to the wrong repository")
    if manifest.get("dependencies"):
        raise AssertionError("bridge must remain independent of optimizer integrations")

    if (ROOT / "dashboards").exists() or (COMPONENT / "dashboards").exists():
        raise AssertionError("optimizer dashboards must not be packaged by the bridge")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    companion_link = "https://github.com/shuffleznl/h3x-energy-" + "arbi" + "trage"
    if readme.count(companion_link) != 1:
        raise AssertionError("README must contain one companion optimizer link")


if __name__ == "__main__":
    main()
