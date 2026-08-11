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
        raise AssertionError("bridge must remain independent of control integrations")

    if (ROOT / "dashboards").exists() or (COMPONENT / "dashboards").exists():
        raise AssertionError("control dashboards must not be packaged by the bridge")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    forbidden = ("nord" + "pool", "arbi" + "trage")
    for reference in forbidden:
        if reference in readme.lower():
            raise AssertionError(
                f"bridge README contains unrelated controller reference: {reference}"
            )

    required_register_documentation = (
        "## Modbus Entity And Register Map",
        "### Inverter Telemetry (Slave 2)",
        "### ESS/BMS Telemetry (Slave 1)",
        "### Writable Controls (Slave 2)",
        "### Time-Slot And Clock Registers (Slave 2)",
        "`40901` (`0x9FC5`)",
        "`40907` (`0x9FCB`)",
        "`5174` (`0x1436`)",
    )
    for reference in required_register_documentation:
        if reference not in readme:
            raise AssertionError(
                f"bridge README is missing Modbus register documentation: {reference}"
            )


if __name__ == "__main__":
    main()
