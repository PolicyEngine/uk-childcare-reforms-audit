"""Analysis: Extend funded weeks from 38 to up to 52 per year."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    row,
    print_references,
)

ANALYSIS = "extend_weeks"


def run(baseline, year):
    y = str(year)
    print("  Currently 38 weeks (term-time); IPPR proposes 48")

    results = run_scenarios(
        {
            "Baseline (38 weeks)": {},
            "44 weeks": {
                "gov.dfe.weeks_per_year": {y: 44},
            },
            "48 weeks (IPPR)": {
                "gov.dfe.weeks_per_year": {y: 48},
            },
            "52 weeks (full year)": {
                "gov.dfe.weeks_per_year": {y: 52},
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
    base = results["Baseline (38 weeks)"]["Combined"]
    for sc, totals in results.items():
        for label in ["UCE", "TCE", "ECE", "Combined"]:
            rows.append(
                row(ANALYSIS, sc, label, totals[label])
            )
        if sc != "Baseline (38 weeks)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print(
        "    Res Foundation: 25hrs/47wks for 3-4yr "
        "costs ~£2.1bn [1]"
    )
    print(
        "    IPPR: 48 weeks per year as part of "
        "childcare guarantee [2]"
    )

    print_references([
        (
            "Resolution Foundation - An Equal Start "
            "(childcare reform proposal)",
            "https://www.resolutionfoundation.org/publications/"
            "an-equal-start/",
        ),
        (
            "IPPR - A Childcare Guarantee",
            "https://www.ippr.org/articles/"
            "a-childcare-guarantee",
        ),
        (
            "DfE - Early Education and Childcare: Statutory "
            "Guidance (term-time definition)",
            "https://www.gov.uk/government/publications/"
            "early-education-and-childcare--2",
        ),
    ])

    return rows


def main():
    args = parse_args("Extend weeks per year")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
