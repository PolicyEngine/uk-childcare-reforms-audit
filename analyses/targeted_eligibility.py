"""Analysis: Expand targeted childcare to more 2-year-olds."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    reform_sim,
    fmt,
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

    # ── Like-for-like: Sutton Trust ────────────────────────
    # Sutton Trust costs giving 30hrs to disadvantaged
    # 2-year-olds at £165m/yr. This is a DIFFERENT reform:
    # they extend the extended_childcare_entitlement to
    # targeted 2yr-olds. PE's analysis here raises the
    # income threshold for the 15hr targeted entitlement.
    # We record the external benchmark for comparison.
    rows.append(
        row(ANALYSIS, "Sutton Trust (30hrs for disadv 2yr-olds)",
            "external", 165e6)
    )

    # Separate Sutton Trust estimate: universalise 30hrs
    # (remove work req for 3-4yr-olds) = £250m/yr
    rows.append(
        row(ANALYSIS, "Sutton Trust (universalise 30hrs, 3-4yr)",
            "external", 250e6)
    )

    print("\n  External comparison:")
    print(
        "    Sutton Trust: Extending 30hrs to "
        "disadvantaged 2-year-olds costs £165m/yr [1]"
    )
    print(
        "    NOTE: Sutton Trust reform extends 30hrs "
        "(extended entitlement) to targeted 2yr-olds. "
        "PE here models raising income limit for the "
        "15hr targeted entitlement — a different reform."
    )
    print(
        "    Sutton Trust: Universalising 30hrs for "
        "all 3-4yr-olds (remove work req) costs "
        "£250m/yr [1]"
    )
    print(
        "    DfE: ~72% of eligible 2-year-olds take up "
        "funded places [2]"
    )
    print(
        "    IFS: Only 13% of eligible families in "
        "bottom third benefit from new entitlements [3]"
    )

    print_references([
        (
            "Sutton Trust / IFS - A Fair Start? and "
            "Opportunity for All (£165m for 2yr-olds, "
            "£250m universalise 30hrs)",
            "https://www.suttontrust.com/our-research/"
            "a-fair-start-equalising-access-to-"
            "early-education/",
        ),
        (
            "DfE - Education Provision: Children Under 5 "
            "(takeup by age)",
            "https://explore-education-statistics.service.gov.uk/"
            "find-statistics/"
            "education-provision-children-under-5",
        ),
        (
            "IFS - New childcare entitlements have "
            "little to offer poorest families",
            "https://ifs.org.uk/news/"
            "new-childcare-entitlements-have-little-"
            "offer-poorest-families",
        ),
        (
            "DfE - Free Early Education for 2-Year-Olds "
            "Guidance",
            "https://www.gov.uk/help-with-childcare-costs/"
            "free-childcare-2-year-olds",
        ),
    ])

    return rows


def main():
    args = parse_args("Expand targeted childcare eligibility")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
