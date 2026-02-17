"""Analysis: Extend funded weeks from 38 to up to 52 per year."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    reform_sim,
    fmt,
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
            "47 weeks (ResFound like-for-like)": {
                "gov.dfe.weeks_per_year": {y: 47},
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

    # Record external benchmark for like-for-like
    rows.append(
        row(ANALYSIS, "ResFound like-for-like (25hrs/47wks)",
            "external", 2.1e9)
    )

    print("\n  External comparison:")
    print(
        "    Res Foundation: 25hrs/47wks for 3-4yr "
        "costs ~£2.1bn [1]"
    )
    print(
        "    PE '47 weeks' scenario uses current 30hrs "
        "for all entitled ages (broader scope than "
        "ResFound's 25hrs for 3-4yr-olds)"
    )
    print(
        "    IPPR: 48 weeks per year as part of "
        "childcare guarantee (£17.8bn gross total) [2]"
    )
    print(
        "    Holiday childcare costs average "
        "£150/wk per child (Coram 2024) [3]"
    )
    print(
        "    IFS: Five-sixths of new entitlement "
        "spending substitutes for private spend [4]"
    )

    print_references([
        (
            "Resolution Foundation - An Equal Start "
            "(25hrs/47wks = £2.1bn)",
            "https://www.resolutionfoundation.org/publications/"
            "an-equal-start/",
        ),
        (
            "IPPR / Save the Children - A Childcare "
            "Guarantee (48 wks, £17.8bn gross)",
            "https://www.ippr.org/articles/"
            "a-childcare-guarantee",
        ),
        (
            "Coram - Childcare Survey 2024 "
            "(holiday costs £150/wk)",
            "https://www.coram.org.uk/resource/"
            "childcare-survey-2024",
        ),
        (
            "IFS - Popularity of new childcare "
            "entitlements (five-sixths substitution)",
            "https://ifs.org.uk/articles/"
            "popularity-new-childcare-entitlements-"
            "could-leave-spending-much-higher-"
            "initially-forecast",
        ),
    ])

    return rows


def main():
    args = parse_args("Extend weeks per year")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
