"""Analysis: Increase UC childcare coverage rate from 85%."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    reform_sim,
    fmt,
    row,
    print_references,
)

ANALYSIS = "uc_coverage"


def run(baseline, year):
    y = str(year)
    print("  UC childcare element covers 85% of costs (since 2023).")
    print("  Multiple orgs recommend moving to 100%.")

    results = run_scenarios(
        {
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
        },
        [("UC CC", "uc_childcare_element")],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline (85%)"]["Combined"]
    for sc, totals in results.items():
        rows.append(
            row(ANALYSIS, sc, "uc_childcare_element",
                totals["Combined"])
        )
        if sc != "Baseline (85%)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    # ── Like-for-like: CPAG (85%→100%, 2024) ──────────────
    # CPAG costs 85%→100% at £150m. They base this on the
    # ~160k households currently claiming (13% of eligible).
    # PE models the full eligible population.
    # Run at year 2024 to match CPAG's costing period.
    lfl_year = 2024
    lfl_y = str(lfl_year)
    lfl_base = float(
        baseline.calculate("uc_childcare_element", lfl_year).sum()
    )
    lfl_sim = reform_sim({
        "gov.dwp.universal_credit.elements.childcare"
        ".coverage_rate": {lfl_y: 1.0},
    })
    lfl_reform = float(
        lfl_sim.calculate("uc_childcare_element", lfl_year).sum()
    )
    lfl_delta = lfl_reform - lfl_base
    print(f"\n  ── Like-for-like: CPAG (year {lfl_year}) ──")
    print(f"    PE  (85%→100%, {lfl_year}): delta {fmt(lfl_delta, 'bn')}")
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
