#!/usr/bin/env python
"""
UK Childcare Reforms Audit - CLI entry point.

Usage:
    python run.py --list                          # List available analyses
    python run.py baseline                        # Run baseline (default year 2026)
    python run.py uc_coverage --year 2025         # Run one analysis for 2025
    python run.py uc_caps uc_coverage             # Run multiple analyses
    python run.py all                             # Run everything
    python run.py all --year 2027                 # Run everything for 2027

Results are saved to output/results_{year}.csv
"""

import argparse
import csv
import os
import sys
from datetime import datetime

from analyses.utils import get_baseline, DEFAULT_YEAR

from analyses import (
    baseline as mod_baseline,
    takeup_sensitivity as mod_takeup,
    uc_caps as mod_uc_caps,
    uc_coverage as mod_uc_coverage,
    extended_hours as mod_extended_hours,
    tfc_rate as mod_tfc_rate,
    tfc_caps as mod_tfc_caps,
    income_cap as mod_income_cap,
    funding_rates as mod_funding_rates,
    targeted_eligibility as mod_targeted,
    extend_weeks as mod_weeks,
    min_work_hours as mod_min_hours,
    net_fiscal_impact as mod_fiscal,
    distributional as mod_distributional,
    wbg_true_cost as mod_wbg_true_cost,
    ifs_min_wage_comp as mod_ifs_min_wage,
    ifs_entitlement_forecast as mod_ifs_forecast,
)

# ── Analysis registry ────────────────────────────────────────────

ANALYSES = {
    "baseline": (
        "Baseline childcare spending",
        mod_baseline,
    ),
    "takeup": (
        "Takeup sensitivity analysis",
        mod_takeup,
    ),
    "uc_caps": (
        "UC childcare caps (+50%, double)",
        mod_uc_caps,
    ),
    "uc_coverage": (
        "UC coverage rate (85% -> 100%)",
        mod_uc_coverage,
    ),
    "extended_hours": (
        "Extended childcare hours (30/40hrs)",
        mod_extended_hours,
    ),
    "tfc_rate": (
        "TFC contribution rate (20% -> 50%)",
        mod_tfc_rate,
    ),
    "tfc_caps": (
        "TFC annual caps (double)",
        mod_tfc_caps,
    ),
    "income_cap": (
        "Remove £100k income cap",
        mod_income_cap,
    ),
    "funding_rates": (
        "DfE funding rates (+20/50/100%)",
        mod_funding_rates,
    ),
    "targeted": (
        "Targeted childcare eligibility",
        mod_targeted,
    ),
    "weeks": (
        "Weeks per year (38 -> 52)",
        mod_weeks,
    ),
    "min_hours": (
        "Minimum work hours (16 -> 1)",
        mod_min_hours,
    ),
    "fiscal": (
        "Net fiscal impact of combined reforms",
        mod_fiscal,
    ),
    "distributional": (
        "Distributional analysis by decile",
        mod_distributional,
    ),
    "wbg_true_cost": (
        "WBG true cost provider rates by age band",
        mod_wbg_true_cost,
    ),
    "ifs_min_wage": (
        "IFS compensate providers for min wage rises",
        mod_ifs_min_wage,
    ),
    "ifs_forecast": (
        "IFS revised entitlement cost forecast",
        mod_ifs_forecast,
    ),
}

CSV_COLUMNS = ["analysis", "scenario", "metric", "value", "year"]


def list_analyses():
    print("\nAvailable analyses:\n")
    for key, (desc, _) in ANALYSES.items():
        print(f"  {key:22s}  {desc}")
    print(f"\n  {'all':22s}  Run all of the above")
    print(f"\nDefault year: {DEFAULT_YEAR}")
    print("Override with --year YYYY\n")


def write_csv(all_rows, year, out_path):
    """Write collected rows to CSV."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for r in all_rows:
            if "year" not in r:
                r["year"] = year
            writer.writerow(r)
    print(f"\nCSV saved: {out_path}  ({len(all_rows)} rows)")


def main():
    parser = argparse.ArgumentParser(
        description="UK Childcare Reforms Audit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python run.py baseline\n"
            "  python run.py uc_coverage --year 2025\n"
            "  python run.py uc_caps uc_coverage tfc_rate\n"
            "  python run.py all --year 2027\n"
            "  python run.py --list"
        ),
    )
    parser.add_argument(
        "analyses",
        nargs="*",
        help="Analysis/analyses to run (see --list)",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=DEFAULT_YEAR,
        help=f"Simulation year (default: {DEFAULT_YEAR})",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available analyses and exit",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Custom CSV output path (default: output/results_{year}.csv)",
    )
    args = parser.parse_args()

    if args.list:
        list_analyses()
        return

    if not args.analyses:
        parser.print_help()
        print()
        list_analyses()
        return

    if "all" in args.analyses:
        selected = list(ANALYSES.keys())
    else:
        selected = args.analyses
        for key in selected:
            if key not in ANALYSES:
                print(f"Unknown analysis: '{key}'")
                print("Use --list to see available analyses.")
                sys.exit(1)

    year = args.year
    out_path = args.csv or f"output/results_{year}.csv"

    print("=" * 70)
    print("UK CHILDCARE REFORMS AUDIT")
    print(
        f"Year: {year} | "
        f"Run: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    print("=" * 70)

    sim = get_baseline()

    all_rows = []
    for key in selected:
        desc, mod = ANALYSES[key]
        print(f"\n{'─' * 70}")
        print(f"  {desc}")
        print(f"{'─' * 70}")
        rows = mod.run(sim, year)
        if rows:
            all_rows.extend(rows)

    # Write CSV
    write_csv(all_rows, year, out_path)

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
