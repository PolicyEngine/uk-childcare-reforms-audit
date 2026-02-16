"""Analysis: Reduce minimum work hours requirement."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    row,
    print_references,
)

ANALYSIS = "min_work_hours"


def run(baseline, year):
    y = str(year)
    print("  Currently 16 hrs/week for ECE and TFC eligibility")
    print("  Res Foundation: excludes many part-time workers")

    results = run_scenarios(
        {
            "Baseline (16 hrs)": {},
            "12 hrs/week": {
                "gov.dfe.extended_childcare_entitlement"
                ".minimum_weekly_hours": {y: 12},
                "gov.hmrc.tax_free_childcare"
                ".minimum_weekly_hours": {y: 12},
            },
            "8 hrs/week": {
                "gov.dfe.extended_childcare_entitlement"
                ".minimum_weekly_hours": {y: 8},
                "gov.hmrc.tax_free_childcare"
                ".minimum_weekly_hours": {y: 8},
            },
            "No minimum (1 hr)": {
                "gov.dfe.extended_childcare_entitlement"
                ".minimum_weekly_hours": {y: 1},
                "gov.hmrc.tax_free_childcare"
                ".minimum_weekly_hours": {y: 1},
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
    base = results["Baseline (16 hrs)"]["Combined"]
    for sc, totals in results.items():
        for label in ["ECE", "TFC", "Combined"]:
            rows.append(
                row(ANALYSIS, sc, label, totals[label])
            )
        if sc != "Baseline (16 hrs)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print(
        "    Res Foundation: Part-time cleaners (10 hrs) "
        "lose £7/wk vs not working [1]"
    )
    print(
        "    TUC: Work conditionality excludes lowest-income "
        "families who need support most [2]"
    )

    print_references([
        (
            "Resolution Foundation - Costly Childcare "
            "(part-time workers)",
            "https://www.resolutionfoundation.org/publications/"
            "costly-childcare/",
        ),
        (
            "TUC - Childcare and Working Families Report",
            "https://www.tuc.org.uk/research-analysis/reports/"
            "childcare-and-working-families",
        ),
        (
            "DfE - 30 Hours Free Childcare: Eligibility "
            "(work requirement)",
            "https://www.gov.uk/30-hours-free-childcare",
        ),
    ])

    return rows


def main():
    args = parse_args("Reduce minimum work hours")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
