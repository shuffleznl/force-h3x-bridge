#!/usr/bin/env python3
"""Validate the bundled Pylontech H3X energy dashboard wiring."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboards" / "pylontech-h3x-energy.yaml"
REMOVED_DASHBOARD = ROOT / "dashboards" / (
    "pylontech-h3x-energy-" + "plot" + "ly.yaml"
)


def read(path: Path) -> str:
    """Read a UTF-8 text file."""
    return path.read_text(encoding="utf-8")


def require(source: str, token: str, label: str) -> None:
    """Require a token in source text."""
    if token not in source:
        raise AssertionError(f"{label} missing {token!r}")


def reject(source: str, token: str, label: str) -> None:
    """Reject a token in source text."""
    if token.lower() in source.lower():
        raise AssertionError(f"{label} still contains {token!r}")


def main() -> None:
    """Run dashboard checks."""
    if not DASHBOARD.exists():
        raise AssertionError("default energy dashboard is missing")
    if REMOVED_DASHBOARD.exists():
        raise AssertionError("secondary dashboard variant must be removed")

    dashboard = read(DASHBOARD)
    dashboards_readme = read(ROOT / "dashboards" / "README.md")
    root_readme = read(ROOT / "README.md")
    combined_docs = dashboards_readme + "\n" + root_readme

    for token in (
        "plot" + "ly",
        "custom:plot" + "ly",
        "pylontech-h3x-energy-plot" + "ly",
    ):
        reject(dashboard, token, "dashboard")
        reject(combined_docs, token, "dashboard docs")

    for token in (
        "select.pylontech_h3x_energy_arbitrage_pv_orientation",
        "number.pylontech_h3x_energy_arbitrage_pv_panel_count",
        "number.pylontech_h3x_energy_arbitrage_pv_panel_wp_rating",
        "number.pylontech_h3x_energy_arbitrage_pv_inverter_limit",
        "sensor.pylontech_h3x_energy_arbitrage_home_load_power",
        "sensor.pylontech_h3x_energy_arbitrage_solar_power",
        "sensor.pylontech_h3x_energy_arbitrage_forecast_load_power",
        "sensor.pylontech_h3x_energy_arbitrage_forecast_solar_power",
        "sensor.pylontech_h3x_energy_arbitrage_planned_grid_charge_energy",
        "sensor.pylontech_h3x_energy_arbitrage_planned_solar_charge_energy",
        "sensor.pylontech_h3x_energy_arbitrage_planned_self_consumption_energy",
        "sensor.pylontech_h3x_energy_arbitrage_planned_battery_export_energy",
        "sensor.pylontech_h3x_energy_arbitrage_forecast_load_energy",
        "sensor.pylontech_h3x_energy_arbitrage_forecast_solar_energy",
        "load_forecast",
        "solar_forecast",
        "net_grid_without_battery_w",
        "net_grid_with_battery_w",
        "grid_charge_kwh",
        "solar_charge_kwh",
        "self_consumption_kwh",
        "battery_export_kwh",
    ):
        require(dashboard, token, "dashboard")

    require(dashboards_readme, "`v0.7.0` or newer", "dashboard README")
    require(root_readme, "Shelly/SMA load and solar data", "root README")


if __name__ == "__main__":
    main()
