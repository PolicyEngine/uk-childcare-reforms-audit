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
        "    HMRC: TFC cost £632m in 2024-25 "
        "(826k families) [1]"
    )
    print(
        "    HMRC: Average annual top-up ~£766 per "
        "family (£632m / 826k), well below £2k cap [1]"
    )
    print(
        "    HMRC: Average monthly top-up £91-93 "
        "(Q3 2025), suggesting most don't hit cap [1]"
    )
    print(
        "    OBR: Originally forecast TFC at £1bn/yr "
        "by 2021-22; never achieved [2]"
    )

    print_references([
        (
            "HMRC - Tax-Free Childcare Statistics "
            "September 2025 (£632m, £91-93/mo avg)",
            "https://www.gov.uk/government/statistics/"
            "tax-free-childcare-statistics-september-2025",
        ),
        (
            "Early Years Alliance / OBR - TFC "
            "underspend (forecast £1bn/yr, actual £236m "
            "in 2019-20)",
            "https://www.eyalliance.org.uk/news/2021/11/"
            "new-data-reveals-huge-tax-free-childcare-"
            "underspend",
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
