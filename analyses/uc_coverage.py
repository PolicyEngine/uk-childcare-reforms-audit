"""Analysis: Increase UC childcare coverage rate from 85%.

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

ANALYSIS = "uc_coverage"


def _uc_total(sim, year):
    """Total universal_credit payments."""
    return float(sim.calculate("universal_credit", year).sum())


def run(baseline, year):
    y = str(year)
    print("  UC childcare element covers 85% of costs (since 2023).")
    print("  Multiple orgs recommend moving to 100%.")
    print("  Measuring net change in total UC payments (post-taper).")

    scenarios = {
        "Baseline (85%)": {},
        "90% coverage": {
            "gov.dwp.universal_credit.elements.childcare"
            ".coverage_rate": {y: 0.90},
        },
        "95% coverage": {
            "gov.dwp.universal_credit.elements.childcare"
            ".coverage_rate": {y: 0.95},
        },
        "100% coverage": {
            "gov.dwp.universal_credit.elements.childcare"
            ".coverage_rate": {y: 1.0},
        },
    }

    # Calculate total UC payments for each scenario
    uc_totals = {}
    for sc_name, params in scenarios.items():
        if params:
            sim = reform_sim(params)
        else:
            sim = baseline
        uc_totals[sc_name] = _uc_total(sim, year)

    base_uc = uc_totals["Baseline (85%)"]

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
        if sc_name != "Baseline (85%)":
            rows.append(
                row(ANALYSIS, sc_name, "delta", delta)
            )

    # Also show gross element for reference
    gross_base = float(
        baseline.calculate("uc_childcare_element", year).sum()
    )
    reform_100 = reform_sim({
        "gov.dwp.universal_credit.elements.childcare"
        ".coverage_rate": {y: 1.0},
    })
    gross_100 = float(
        reform_100.calculate("uc_childcare_element", year).sum()
    )
    print(f"\n    (Gross element for reference: "
          f"baseline {fmt(gross_base, 'bn')}, "
          f"100%: {fmt(gross_100, 'bn')}, "
          f"gross delta: {fmt(gross_100 - gross_base, 'bn')})")

    # ── Like-for-like: CPAG (85%→100%, 2024) ──────────────
    # CPAG costs 85%→100% at £150m. They base this on the
    # ~160k households currently claiming (13% of eligible).
    # PE models the full eligible population.
    # Run at year 2024 to match CPAG's costing period.
    lfl_year = 2024
    lfl_y = str(lfl_year)
    lfl_base_uc = _uc_total(baseline, lfl_year)
    lfl_sim = reform_sim({
        "gov.dwp.universal_credit.elements.childcare"
        ".coverage_rate": {lfl_y: 1.0},
    })
    lfl_reform_uc = _uc_total(lfl_sim, lfl_year)
    lfl_delta = lfl_reform_uc - lfl_base_uc
    print(f"\n  ── Like-for-like: CPAG (year {lfl_year}) ──")
    print(f"    PE  (85%→100%, {lfl_year}): net UC delta {fmt(lfl_delta, 'bn')}")
    print(f"    CPAG estimate:             £150m")
    print(f"    Note: CPAG covers ~160k current claimants (13%);")
    print(f"          PE models full eligible population")
    rows.append(
        row(ANALYSIS, "CPAG like-for-like (100%, 2024)",
            "delta", lfl_delta, year=lfl_year)
    )
    rows.append(
        row(ANALYSIS, "CPAG like-for-like (100%, 2024)",
            "external", 150e6, year=lfl_year)
    )

    print("\n  External comparison:")
    print("    CPAG: 85%->100% coverage costs £150m initially [1]")
    print("    Res Foundation: recommend 100% coverage [2]")
    print("    IPPR: recommend 100% coverage [3]")
    print(
        "    DWP: UC CC element ~£850m annualised "
        "(160k HHs, £420/mo avg, Aug 2025) [4]"
    )
    print(
        "    DWP: Only 13% of eligible UC families "
        "claim the childcare element [4]"
    )

    print_references([
        (
            "CPAG - Universal Credit: A Three-Step Plan "
            "(2024, costs 85%->100% at £150m)",
            "https://cpag.org.uk/news/"
            "universal-credit-three-step-plan",
        ),
        (
            "Resolution Foundation - Costly Childcare "
            "(June 2023)",
            "https://www.resolutionfoundation.org/publications/"
            "costly-childcare/",
        ),
        (
            "IPPR - Childcare Guarantee (2024)",
            "https://www.ippr.org/articles/"
            "a-childcare-guarantee",
        ),
        (
            "DWP - UC Childcare Element Statistics "
            "to August 2025 (160k HHs, £420/mo, 13% takeup)",
            "https://www.gov.uk/government/statistics/"
            "universal-credit-statistics-29-april-2013-"
            "to-9-october-2025",
        ),
        (
            "The Universal Credit (Childcare Costs) "
            "Regulations 2023",
            "https://www.legislation.gov.uk/uksi/2023/752/"
            "contents/made",
        ),
    ])

    return rows


def main():
    args = parse_args("Increase UC childcare coverage rate")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
