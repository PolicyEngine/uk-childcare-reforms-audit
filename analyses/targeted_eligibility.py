"""Analysis: Expand targeted childcare to more 2-year-olds."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    row,
    print_references,
)

ANALYSIS = "targeted_eligibility"


def run(baseline, year):
    y = str(year)
    print(
        "  Current: UC income <£15,400 "
        "or TC income <£16,190"
    )
    print("  ~72% of eligible 2-year-olds take up places")

    results = run_scenarios(
        {
            "Baseline": {},
            "UC limit £20k": {
                "gov.dfe.targeted_childcare_entitlement"
                ".income_limit.universal_credit": {y: 20_000},
            },
            "UC limit £25k": {
                "gov.dfe.targeted_childcare_entitlement"
                ".income_limit.universal_credit": {y: 25_000},
            },
            "UC limit £30k": {
                "gov.dfe.targeted_childcare_entitlement"
                ".income_limit.universal_credit": {y: 30_000},
            },
        },
        [("TCE", "targeted_childcare_entitlement")],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline"]["Combined"]
    for sc, totals in results.items():
        rows.append(
            row(ANALYSIS, sc,
                "targeted_childcare_entitlement",
                totals["Combined"])
        )
        if sc != "Baseline":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print(
        "    DfE: ~72% of eligible 2-year-olds take up "
        "funded places [1]"
    )
    print(
        "    DfE: Eligibility criteria for 2-year-old "
        "entitlement [2]"
    )

    print_references([
        (
            "DfE - Education Provision: Children Under 5 "
            "(takeup by age)",
            "https://explore-education-statistics.service.gov.uk/"
            "find-statistics/"
            "education-provision-children-under-5",
        ),
        (
            "DfE - Free Early Education for 2-Year-Olds "
            "Guidance",
            "https://www.gov.uk/help-with-childcare-costs/"
            "free-childcare-2-year-olds",
        ),
        (
            "The Local Authority (Duty to Secure Early Years "
            "Provision Free of Charge) Regulations 2014",
            "https://www.legislation.gov.uk/uksi/2014/2147/"
            "contents/made",
        ),
    ])

    return rows


def main():
    args = parse_args("Expand targeted childcare eligibility")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
