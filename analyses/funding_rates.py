"""Analysis: Increase DfE childcare funding rates."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    row,
    print_references,
)

ANALYSIS = "funding_rates"


def run(baseline, year):
    y = str(year)
    print(
        "  Current: Age <2: £11.22/hr, "
        "Age 2: £8.28/hr, Age 3+: £5.88/hr"
    )
    print("  WBG estimates a £5.2bn funding gap in 2025-26")

    results = run_scenarios(
        {
            "Baseline": {},
            "+20% rates": {
                "gov.dfe.childcare_funding_rate[0].amount": {
                    y: 13.46
                },
                "gov.dfe.childcare_funding_rate[1].amount": {
                    y: 9.94
                },
                "gov.dfe.childcare_funding_rate[2].amount": {
                    y: 7.06
                },
            },
            "+50% rates": {
                "gov.dfe.childcare_funding_rate[0].amount": {
                    y: 16.83
                },
                "gov.dfe.childcare_funding_rate[1].amount": {
                    y: 12.42
                },
                "gov.dfe.childcare_funding_rate[2].amount": {
                    y: 8.82
                },
            },
            "Double rates": {
                "gov.dfe.childcare_funding_rate[0].amount": {
                    y: 22.44
                },
                "gov.dfe.childcare_funding_rate[1].amount": {
                    y: 16.56
                },
                "gov.dfe.childcare_funding_rate[2].amount": {
                    y: 11.76
                },
            },
        },
        [
            ("UCE", "universal_childcare_entitlement"),
            ("TCE", "targeted_childcare_entitlement"),
            ("ECE", "extended_childcare_entitlement"),
        ],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline"]["Combined"]
    for sc, totals in results.items():
        for label in ["UCE", "TCE", "ECE", "Combined"]:
            rows.append(
                row(ANALYSIS, sc, label, totals[label])
            )
        if sc != "Baseline":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print("    WBG: Total needed £9.4bn (gap of £5.2bn) [1]")
    print(
        "    DfE: Published hourly funding rates for "
        "2024-25 and 2025-26 [2]"
    )

    print_references([
        (
            "Women's Budget Group - Childcare Funding Gap "
            "Analysis",
            "https://wbg.org.uk/analysis/"
            "the-childcare-funding-gap/",
        ),
        (
            "DfE - Early Years Funding Rates 2024-25",
            "https://www.gov.uk/government/publications/"
            "early-years-funding-2024-to-2025",
        ),
        (
            "IFS - Annual Report on Education Spending "
            "(Early Years Chapter)",
            "https://ifs.org.uk/publications/"
            "annual-report-education-spending-england-2025-26",
        ),
        (
            "Ceeda/DfE - Provider Cost Study 2024",
            "https://www.gov.uk/government/publications/"
            "early-years-provider-cost-study-2024",
        ),
    ])

    return rows


def main():
    args = parse_args("Increase DfE funding rates")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
