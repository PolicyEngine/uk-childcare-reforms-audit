"""Analysis: Increase UC childcare element caps."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
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

    print("\n  External comparison:")
    print(
        "    Res Foundation: removing caps would help "
        "families with high childcare costs [1]"
    )
    print(
        "    DWP: caps last uprated in 2023 alongside "
        "coverage increase to 85% [2]"
    )

    print_references([
        (
            "Resolution Foundation - Costly Childcare "
            "(June 2023)",
            "https://www.resolutionfoundation.org/publications/"
            "costly-childcare/",
        ),
        (
            "DWP - Benefit and Pension Rates "
            "(UC childcare caps)",
            "https://www.gov.uk/government/publications/"
            "benefit-and-pension-rates-2024-to-2025",
        ),
        (
            "The Universal Credit Regulations 2013 "
            "(Reg 34 - childcare costs)",
            "https://www.legislation.gov.uk/uksi/2013/376/"
            "regulation/34",
        ),
    ])

    return rows


def main():
    args = parse_args("Increase UC childcare caps")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
