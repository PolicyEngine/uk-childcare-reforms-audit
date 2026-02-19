"""Analysis: Increase UC childcare element caps.

Measures the net change in actual UC payments (post-taper) rather than
the gross uc_childcare_element (pre-taper component), since the 55%
earnings taper means the fiscal cost is lower than the gross element.
"""

from .utils import (
    get_baseline,
    parse_args,
    reform_sim,
    fmt,
    row,
    print_references,
)

ANALYSIS = "uc_caps"


def _uc_total(sim, year):
    """Total universal_credit payments."""
    return float(sim.calculate("universal_credit", year).sum())


def run(baseline, year):
    y = str(year)
    print("  Current caps: £1,014.63 (1 child), £1,739.37 (2+)")
    print("  Measuring net change in total UC payments (post-taper).")

    scenarios = {
        "Baseline": {},
        "+50% caps": {
            "gov.dwp.universal_credit.elements.childcare"
            ".cap.1": {y: 1547.82},
            "gov.dwp.universal_credit.elements.childcare"
            ".cap.2": {y: 2653.41},
        },
        "Double caps": {
            "gov.dwp.universal_credit.elements.childcare"
            ".cap.1": {y: 2063.76},
            "gov.dwp.universal_credit.elements.childcare"
            ".cap.2": {y: 3537.88},
        },
    }

    uc_totals = {}
    for sc_name, params in scenarios.items():
        if params:
            sim = reform_sim(params)
        else:
            sim = baseline
        uc_totals[sc_name] = _uc_total(sim, year)

    base_uc = uc_totals["Baseline"]

    rows = []
    for sc_name in scenarios:
        delta = uc_totals[sc_name] - base_uc
        print(
            f"    {sc_name:50s} "
            f"UC: {fmt(uc_totals[sc_name], 'bn'):>12s}"
            f"  delta: {fmt(delta, 'bn')}"
        )
        rows.append(
            row(ANALYSIS, sc_name, "universal_credit",
                uc_totals[sc_name])
        )
        if sc_name != "Baseline":
            rows.append(
                row(ANALYSIS, sc_name, "delta", delta)
            )

    # ── Like-for-like: HMT 2023 cap uprating ────────────
    # HMT costed raising caps from £646.35/£1,108.04 →
    # £950.92/£1,630.15 at £50-85m/yr (midpoint £67.5m).
    # We create a "pre-uprating" sim with old caps at 2023,
    # and compare to PE 2023 baseline (which has new caps).
    lfl_year = 2023
    lfl_y = str(lfl_year)
    old_caps_sim = reform_sim({
        "gov.dwp.universal_credit.elements.childcare"
        ".cap.1": {lfl_y: 646.35},
        "gov.dwp.universal_credit.elements.childcare"
        ".cap.2": {lfl_y: 1108.04},
    })
    old_uc = _uc_total(old_caps_sim, lfl_year)
    new_uc = _uc_total(baseline, lfl_year)
    lfl_delta = new_uc - old_uc
    print(f"\n  ── Like-for-like: HMT 2023 uprating ──")
    print(f"    PE  (£646→£951 / £1,108→£1,630, {lfl_year}): "
          f"delta {fmt(lfl_delta, 'bn')}")
    print(f"    HMT estimate: £50-85m/yr (midpoint £67.5m)")
    rows.append(
        row(ANALYSIS, "HMT 2023 uprating like-for-like",
            "delta", lfl_delta, year=lfl_year)
    )
    rows.append(
        row(ANALYSIS, "HMT 2023 uprating like-for-like",
            "external", 67.5e6, year=lfl_year)
    )

    print("\n  External comparison:")
    print(
        "    HM Treasury: 2023 cap uprating "
        "(£646/£1,108 -> £951/£1,630) cost "
        "£50-85m/yr (OBR-certified) [1]"
    )
    print(
        "    DWP: Only 3% of UC CC households "
        "hit the maximum cap [2]"
    )
    print(
        "    DWP: Average monthly UC CC amount "
        "£420 nationally, £700 in London [2]"
    )
    print(
        "    IFS: UC CC caps frozen 2005-2023, "
        "real-terms cut of 56% [3]"
    )
    print(
        "    Budget 2025: From 2026, cap increases "
        "by £736/mo per additional child beyond two [2]"
    )

    print_references([
        (
            "HM Treasury - Spring Budget 2023 Policy "
            "Costings (cap uprating £50-85m/yr)",
            "https://assets.publishing.service.gov.uk/"
            "media/6411603be90e076ccf66d781/"
            "Costing_Document_-_Spring_Budget_2023.pdf",
        ),
        (
            "DWP - UC Childcare Element Statistics "
            "to August 2025 (3% hit cap, £420/mo avg)",
            "https://www.gov.uk/government/statistics/"
            "universal-credit-statistics-29-april-2013-"
            "to-9-october-2025",
        ),
        (
            "IFS - The Changing Cost of Childcare "
            "(caps frozen 2005-2023, 56% real cut)",
            "https://ifs.org.uk/publications/"
            "changing-cost-childcare",
        ),
        (
            "Resolution Foundation - Costly Childcare "
            "(June 2023)",
            "https://www.resolutionfoundation.org/publications/"
            "costly-childcare/",
        ),
    ])

    return rows


def main():
    args = parse_args("Increase UC childcare caps")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
