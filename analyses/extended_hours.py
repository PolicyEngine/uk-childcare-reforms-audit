"""Analysis: Expand extended childcare hours."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    row,
    print_references,
)

ANALYSIS = "extended_hours"


def run(baseline, year):
    y = str(year)
    print("  Government 2023 expansion phases in 30hrs for ages 9m-4")
    print("  IPPR proposes wrap-around care up to 40+ hrs")

    results = run_scenarios(
        {
            "Baseline (current phased)": {},
            "30hrs all ages 1-4 (full rollout)": {
                "gov.dfe.extended_childcare_entitlement"
                ".hours[1].amount": {y: 30},
                "gov.dfe.extended_childcare_entitlement"
                ".hours[2].amount": {y: 30},
            },
            "40hrs all ages 1-4 (IPPR wrap-around)": {
                "gov.dfe.extended_childcare_entitlement"
                ".hours[1].amount": {y: 40},
                "gov.dfe.extended_childcare_entitlement"
                ".hours[2].amount": {y: 40},
                "gov.dfe.extended_childcare_entitlement"
                ".hours[3].amount": {y: 40},
                "gov.dfe.extended_childcare_entitlement"
                ".hours[4].amount": {y: 40},
            },
        },
        [("ECE", "extended_childcare_entitlement")],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline (current phased)"]["Combined"]
    for sc, totals in results.items():
        rows.append(
            row(ANALYSIS, sc,
                "extended_childcare_entitlement",
                totals["Combined"])
        )
        if sc != "Baseline (current phased)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print(
        "    OBR: 2023 expansion costs £3.3bn in 2025-26, "
        "£4.1bn by 2027-28 [1]"
    )
    print("    IPPR wrap-around (0-11): £17.8bn gross [2]")
    print(
        "\n  NOTE: 30hrs and 40hrs may give identical results "
        "because maximum_extended_childcare_hours_usage "
        "defaults to 30 hrs/week."
    )

    print_references([
        (
            "OBR - Spring Budget 2023 Policy Costings "
            "(Childcare Expansion)",
            "https://obr.uk/docs/dlm_uploads/"
            "Annexes-March-2023.pdf",
        ),
        (
            "IPPR - A Childcare Guarantee (wrap-around "
            "proposal)",
            "https://www.ippr.org/articles/"
            "a-childcare-guarantee",
        ),
        (
            "DfE - Childcare Act 2016 (30 hours entitlement "
            "statutory basis)",
            "https://www.legislation.gov.uk/ukpga/2016/5/"
            "contents",
        ),
        (
            "DfE - Spring Budget 2023: Childcare Expansion "
            "Announcement",
            "https://www.gov.uk/government/news/"
            "spring-budget-2023-childcare-expansion",
        ),
    ])

    return rows


def main():
    args = parse_args("Expand extended childcare hours")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
