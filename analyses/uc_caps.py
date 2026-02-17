"""Analysis: Increase UC childcare element caps."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    reform_sim,
    fmt,
    row,
    print_references,
)

ANALYSIS = "uc_caps"


def run(baseline, year):
    y = str(year)
    print("  Current caps: £1,014.63 (1 child), £1,739.37 (2+)")

    results = run_scenarios(
        {
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
        },
        [("UC CC", "uc_childcare_element")],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline"]["Combined"]
    for sc, totals in results.items():
        rows.append(
            row(ANALYSIS, sc, "uc_childcare_element",
                totals["Combined"])
        )
        if sc != "Baseline":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
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
    old_val = float(
        old_caps_sim.calculate("uc_childcare_element", lfl_year).sum()
    )
    new_val = float(
        baseline.calculate("uc_childcare_element", lfl_year).sum()
    )
    lfl_delta = new_val - old_val
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
