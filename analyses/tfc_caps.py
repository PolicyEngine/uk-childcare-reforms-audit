"""Analysis: Increase TFC annual caps."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    row,
    print_references,
)

ANALYSIS = "tfc_caps"


def run(baseline, year):
    y = str(year)
    print("  Current caps: £2,000/child, £4,000/disabled child")

    results = run_scenarios(
        {
            "Baseline (£2k/£4k)": {},
            "£3k/£6k caps": {
                "gov.hmrc.tax_free_childcare.contribution"
                ".standard_child": {y: 3000},
                "gov.hmrc.tax_free_childcare.contribution"
                ".disabled_child": {y: 6000},
            },
            "£4k/£8k caps (double)": {
                "gov.hmrc.tax_free_childcare.contribution"
                ".standard_child": {y: 4000},
                "gov.hmrc.tax_free_childcare.contribution"
                ".disabled_child": {y: 8000},
            },
        },
        [("TFC", "tax_free_childcare")],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline (£2k/£4k)"]["Combined"]
    for sc, totals in results.items():
        rows.append(
            row(ANALYSIS, sc, "tax_free_childcare",
                totals["Combined"])
        )
        if sc != "Baseline (£2k/£4k)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print(
        "    HMRC: Average quarterly TFC payment ~£400 [1]"
    )
    print(
        "    Childcare Payments Act 2014: sets statutory "
        "framework for TFC [2]"
    )

    print_references([
        (
            "HMRC - Tax-Free Childcare Statistics "
            "September 2025",
            "https://www.gov.uk/government/statistics/"
            "tax-free-childcare-statistics-september-2025",
        ),
        (
            "Childcare Payments Act 2014",
            "https://www.legislation.gov.uk/ukpga/2014/28/"
            "contents",
        ),
    ])

    return rows


def main():
    args = parse_args("Increase TFC annual caps")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
