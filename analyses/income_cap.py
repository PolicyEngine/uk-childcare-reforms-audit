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
            "£120k cap (Govt lower)": {
                "gov.dfe.extended_childcare_entitlement"
                ".income.limit": {y: 120_000},
                "gov.hmrc.tax_free_childcare.income"
                ".income_limit": {y: 120_000},
            },
            "£150k cap": {
                "gov.dfe.extended_childcare_entitlement"
                ".income.limit": {y: 150_000},
                "gov.hmrc.tax_free_childcare.income"
                ".income_limit": {y: 150_000},
            },
            "£160k cap (Govt upper)": {
                "gov.dfe.extended_childcare_entitlement"
                ".income.limit": {y: 160_000},
                "gov.hmrc.tax_free_childcare.income"
                ".income_limit": {y: 160_000},
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

    # Record external benchmark for £120k-£160k range
    rows.append(
        row(ANALYSIS, "Govt estimate (£120k-£160k)",
            "external", 1.4e9)
    )

    print("\n  External comparison:")
    print(
        "    Government: Raising to £120-160k per-parent "
        "threshold would cost £1.4bn (TFC + extended "
        "hours combined) [1]"
    )
    print(
        "    PE £120k cap and £160k cap scenarios "
        "bracket the Government's estimate"
    )
    print(
        "    IFS: Higher earners benefit disproportionately "
        "from TFC vs UC families [2]"
    )
    print(
        "    IFA Magazine: 2023 expansion made the "
        "£100k cliff-edge more punitive [1]"
    )

    print_references([
        (
            "Government estimate (via AJ Bell / IFA "
            "Magazine): £1.4bn for raising to "
            "£120-160k household threshold",
            "https://www.ajbell.co.uk/news/"
            "beat-ps100000-tax-trap-cost-could-cost-"
            "parents-tens-thousands",
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
