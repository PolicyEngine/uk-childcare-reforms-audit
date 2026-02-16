"""Analysis: Increase UC childcare coverage rate from 85%."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
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

    print("\n  External comparison:")
    print("    Res Foundation: recommend 100% coverage [1]")
    print("    IPPR: recommend 100% coverage [2]")
    print(
        "    DWP Stat-Xplore: UC childcare element spend "
        "~£1.0bn in 2023-24 [3]"
    )

    print_references([
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
            "DWP - UC Statistics: Childcare Costs "
            "(Stat-Xplore)",
            "https://stat-xplore.dwp.gov.uk/",
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
