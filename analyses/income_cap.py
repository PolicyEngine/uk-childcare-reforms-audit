"""Analysis: Remove the £100k income cap for extended/TFC childcare."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    row,
    print_references,
)

ANALYSIS = "income_cap"


def run(baseline, year):
    y = str(year)
    print("  Current: £100k adjusted net income cap")
    print("  Tests extending eligibility to higher earners")

    results = run_scenarios(
        {
            "Baseline (£100k cap)": {},
            "£150k cap": {
                "gov.dfe.extended_childcare_entitlement"
                ".income.limit": {y: 150_000},
                "gov.hmrc.tax_free_childcare.income"
                ".income_limit": {y: 150_000},
            },
            "£200k cap": {
                "gov.dfe.extended_childcare_entitlement"
                ".income.limit": {y: 200_000},
                "gov.hmrc.tax_free_childcare.income"
                ".income_limit": {y: 200_000},
            },
            "No cap (£10m)": {
                "gov.dfe.extended_childcare_entitlement"
                ".income.limit": {y: 10_000_000},
                "gov.hmrc.tax_free_childcare.income"
                ".income_limit": {y: 10_000_000},
            },
        },
        [
            ("ECE", "extended_childcare_entitlement"),
            ("TFC", "tax_free_childcare"),
        ],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline (£100k cap)"]["Combined"]
    for sc, totals in results.items():
        for label in ["ECE", "TFC", "Combined"]:
            rows.append(
                row(ANALYSIS, sc, label, totals[label])
            )
        if sc != "Baseline (£100k cap)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print(
        "    HMRC guidance: £100k adjusted net income "
        "threshold [1]"
    )
    print(
        "    IFS: Higher earners benefit disproportionately "
        "from TFC vs UC families [2]"
    )

    print_references([
        (
            "HMRC - Tax-Free Childcare Eligibility Criteria",
            "https://www.gov.uk/tax-free-childcare",
        ),
        (
            "IFS - The health of the early years sector",
            "https://ifs.org.uk/publications/"
            "health-early-years-sector",
        ),
        (
            "DfE - Extended Entitlement Eligibility "
            "(Adjusted Net Income)",
            "https://www.gov.uk/30-hours-free-childcare",
        ),
    ])

    return rows


def main():
    args = parse_args("Remove £100k income cap")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
