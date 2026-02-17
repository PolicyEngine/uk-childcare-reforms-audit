"""Analysis: Reduce minimum work hours requirement."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    reform_sim,
    fmt,
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
            "ECE only no min (Sutton Trust like-for-like)": {
                "gov.dfe.extended_childcare_entitlement"
                ".minimum_weekly_hours": {y: 1},
                # TFC minimum stays at 16 hrs
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

    # Record external benchmark
    rows.append(
        row(ANALYSIS, "Sutton Trust like-for-like (ECE only)",
            "external", 250e6)
    )

    print("\n  External comparison:")
    print(
        "    Sutton Trust: Removing work requirement "
        "for 30hrs (3-4yr-olds) costs £250m/yr [1]"
    )
    print(
        "    PE 'ECE only no min' scenario removes "
        "work requirement for all ECE ages (9m-4), "
        "broader than Sutton Trust's 3-4yr-olds only"
    )
    print(
        "    Sutton Trust: This would extend eligibility "
        "to 80% of children in bottom third of "
        "earnings [1]"
    )
    print(
        "    Res Foundation: Part-time cleaners (10 hrs) "
        "lose £7/wk vs not working [2]"
    )
    print(
        "    CPAG: 16% of families have no earnings "
        "and are the largest excluded group [3]"
    )
    print(
        "    Save the Children: Two-thirds of poorest "
        "families miss out on childcare [3]"
    )

    print_references([
        (
            "Sutton Trust / IFS - Opportunity for All "
            "(£250m/yr to universalise 30hrs, removing "
            "work requirement)",
            "https://www.suttontrust.com/our-research/"
            "a-fair-start-equalising-access-to-"
            "early-education/",
        ),
        (
            "Resolution Foundation - Costly Childcare "
            "(part-time workers)",
            "https://www.resolutionfoundation.org/publications/"
            "costly-childcare/",
        ),
        (
            "CPAG - Access Denied: Childcare Barriers / "
            "Save the Children - Two-thirds of poorest "
            "families miss out",
            "https://cpag.org.uk/sites/default/files/"
            "2024-03/Access_denied_childcare.pdf",
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
