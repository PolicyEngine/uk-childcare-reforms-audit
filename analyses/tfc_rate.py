"""Analysis: Increase Tax-Free Childcare contribution rate."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    row,
    print_references,
)

ANALYSIS = "tfc_rate"


def run(baseline, year):
    y = str(year)
    print("  Currently 20% top-up (£2 for every £8 parents pay)")

    results = run_scenarios(
        {
            "Baseline (20%)": {},
            "25% top-up": {
                "gov.hmrc.tax_free_childcare.contribution"
                ".rate": {y: 0.25},
            },
            "33% top-up": {
                "gov.hmrc.tax_free_childcare.contribution"
                ".rate": {y: 0.33},
            },
            "50% top-up": {
                "gov.hmrc.tax_free_childcare.contribution"
                ".rate": {y: 0.50},
            },
        },
        [("TFC", "tax_free_childcare")],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline (20%)"]["Combined"]
    for sc, totals in results.items():
        rows.append(
            row(ANALYSIS, sc, "tax_free_childcare",
                totals["Combined"])
        )
        if sc != "Baseline (20%)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print(
        "    HMRC: TFC cost £0.5bn in 2024-25, "
        "1.1m families used it [1]"
    )
    print(
        "    IFS: Only ~40% of eligible families aware "
        "of TFC; takeup lower still [2]"
    )

    print_references([
        (
            "HMRC - Tax-Free Childcare Statistics "
            "September 2025",
            "https://www.gov.uk/government/statistics/"
            "tax-free-childcare-statistics-september-2025",
        ),
        (
            "IFS - The health of the early years sector",
            "https://ifs.org.uk/publications/"
            "health-early-years-sector",
        ),
        (
            "HMRC - Tax-Free Childcare Scheme Guidance",
            "https://www.gov.uk/tax-free-childcare",
        ),
    ])

    return rows


def main():
    args = parse_args("Increase TFC contribution rate")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
