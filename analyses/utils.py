"""Shared utilities for childcare reform audit analyses."""

import argparse
from policyengine_uk import Microsimulation, Scenario

DEFAULT_YEAR = 2026
CURRENCY = "£"


def parse_args(description, extra_args_fn=None):
    """Standard argument parser with --year flag."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--year",
        type=int,
        default=DEFAULT_YEAR,
        help=f"Simulation year (default: {DEFAULT_YEAR})",
    )
    if extra_args_fn:
        extra_args_fn(parser)
    return parser.parse_args()


def fmt(value, unit="bn"):
    """Format currency values."""
    if unit == "bn":
        return f"{CURRENCY}{value / 1e9:.2f}bn"
    elif unit == "m":
        return f"{CURRENCY}{value / 1e6:.0f}m"
    return f"{CURRENCY}{value:,.0f}"


def get_baseline():
    """Create and return a baseline Microsimulation."""
    print("Loading baseline microsimulation...")
    return Microsimulation()


def reform_sim(parameter_changes):
    """Create a reformed Microsimulation from parameter changes."""
    scenario = Scenario(parameter_changes=parameter_changes)
    return Microsimulation(scenario=scenario)


def row(analysis, scenario, metric, value):
    """Build a single CSV result row dict."""
    return {
        "analysis": analysis,
        "scenario": scenario,
        "metric": metric,
        "value": value,
    }


def run_scenarios(scenarios, output_vars, baseline, year):
    """
    Run a set of reform scenarios and report results.

    Returns:
        (results_dict, rows_list) where rows_list is
        dashboard-ready row dicts.
    """
    results = {}
    rows = []
    analysis_name = None  # filled by caller if needed

    for scenario_name, params in scenarios.items():
        if params:
            sim = reform_sim(params)
        else:
            sim = baseline

        totals = {}
        for var_label, var_name in output_vars:
            val = float(sim.calculate(var_name, year).sum())
            totals[var_label] = val
        totals["Combined"] = sum(totals.values())
        results[scenario_name] = totals

    # Print and build rows
    for scenario_name, totals in results.items():
        if len(output_vars) == 1:
            label = output_vars[0][0]
            print(
                f"    {scenario_name:50s} "
                f"{fmt(totals[label], 'bn'):>12s}"
            )
        else:
            parts = "  ".join(
                f"{l}: {fmt(totals[l], 'bn')}"
                for l, _ in output_vars
            )
            print(
                f"    {scenario_name:40s} {parts}  "
                f"Total: {fmt(totals['Combined'], 'bn')}"
            )

    baseline_name = list(scenarios.keys())[0]
    base_total = results[baseline_name]["Combined"]
    for scenario_name, totals in results.items():
        if scenario_name != baseline_name:
            diff = totals["Combined"] - base_total
            print(
                f"    {scenario_name:50s} "
                f"delta: {fmt(diff, 'bn')}"
            )

    return results


def print_references(refs):
    """Print a formatted references section."""
    print("\n  References:")
    for i, (title, url) in enumerate(refs, 1):
        print(f"    [{i}] {title}")
        print(f"        {url}")
