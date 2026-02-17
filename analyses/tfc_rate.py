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
        "    HMRC: TFC cost £632m in 2024-25, "
        "826k families [1]"
    )
    print(
        "    HMRC: Average monthly top-up £91-93 "
        "per family (Q3 2025) [1]"
    )
    print(
        "    OBR: TFC cumulative underspend of £2.4bn "
        "vs forecast 2017-2021 [2]"
    )
    print(
        "    REC: Called for doubling top-up from £2 to "
        "£4 per £8 (no cost published) [3]"
    )
    print(
        "    IFS: Only ~40% of eligible families aware "
        "of TFC; takeup lower still [4]"
    )

    print_references([
        (
            "HMRC - Tax-Free Childcare Statistics "
            "September 2025 (£632m, 826k families)",
            "https://www.gov.uk/government/statistics/"
            "tax-free-childcare-statistics-september-2025",
        ),
        (
            "Early Years Alliance / OBR - TFC "
            "underspend of £2.4bn (2017-2021)",
            "https://www.eyalliance.org.uk/news/2021/11/"
            "new-data-reveals-huge-tax-free-childcare-"
            "underspend",
        ),
        (
            "REC - Increase Tax-Free Childcare to "
            "keep parents in work (double top-up proposal)",
            "https://www.rec.uk.com/our-view/news/"
            "press-releases/"
            "increase-tax-free-childcare-keep-parents-"
            "work-rec-tells-chancellor-ahead-budget",
        ),
        (
            "IFS - The health of the early years sector",
            "https://ifs.org.uk/publications/"
            "health-early-years-sector",
        ),
    ])

    return rows


def main():
    args = parse_args("Increase TFC contribution rate")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
