"""Analysis: Increase DfE childcare funding rates."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    reform_sim,
    fmt,
    row,
    print_references,
)

ANALYSIS = "funding_rates"


def run(baseline, year):
    y = str(year)
    print(
        "  Current (2024-25): Age <2: £11.22/hr, "
        "Age 2: £8.28/hr, Age 3+: £5.88/hr"
    )
    print(
        "  DfE 2025-26 rates: Age <2: £11.54/hr, "
        "Age 2: £8.53/hr, Age 3+: £6.12/hr"
    )
    print("  WBG estimates a £5.2bn funding gap in 2025-26")

    results = run_scenarios(
        {
            "Baseline": {},
            "+20% rates": {
                "gov.dfe.childcare_funding_rate[0].amount": {
                    y: 13.46
                },
                "gov.dfe.childcare_funding_rate[1].amount": {
                    y: 9.94
                },
                "gov.dfe.childcare_funding_rate[2].amount": {
                    y: 7.06
                },
            },
            "+50% rates": {
                "gov.dfe.childcare_funding_rate[0].amount": {
                    y: 16.83
                },
                "gov.dfe.childcare_funding_rate[1].amount": {
                    y: 12.42
                },
                "gov.dfe.childcare_funding_rate[2].amount": {
                    y: 8.82
                },
            },
            "Double rates": {
                "gov.dfe.childcare_funding_rate[0].amount": {
                    y: 22.44
                },
                "gov.dfe.childcare_funding_rate[1].amount": {
                    y: 16.56
                },
                "gov.dfe.childcare_funding_rate[2].amount": {
                    y: 11.76
                },
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
    base = results["Baseline"]["Combined"]
    for sc, totals in results.items():
        for label in ["UCE", "TCE", "ECE", "Combined"]:
            rows.append(
                row(ANALYSIS, sc, label, totals[label])
            )
        if sc != "Baseline":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    # Record WBG benchmark
    # WBG says providers need £9.4bn total (current £4.2bn
    # + £5.2bn gap). PE "Double rates" is the closest match
    # (roughly doubling from ~£4.2bn to ~£9.4bn).
    rows.append(
        row(ANALYSIS, "WBG like-for-like (close funding gap)",
            "external_total_needed", 9.4e9)
    )
    rows.append(
        row(ANALYSIS, "WBG like-for-like (close funding gap)",
            "external_gap", 5.2e9)
    )

    print("\n  External comparison:")
    print("    WBG: Total needed £9.4bn (gap of £5.2bn) [1]")
    print(
        "    PE 'Double rates' (£12.95bn) overshoots "
        "WBG target (£9.4bn). PE '+50% rates' (£9.71bn) "
        "is closest to WBG's £9.4bn"
    )
    print(
        "    NAO: DfE early years outturn £6.2bn "
        "in 2024-25, forecast £8.2bn 2025-26 [2]"
    )
    print(
        "    DfE 2025-26 rates: <2: £11.54/hr (+3.4%), "
        "2: £8.53/hr (+3.3%), 3+: £6.12/hr (+4.1%) [3]"
    )
    print(
        "    DfE: Additional £75m revenue funding "
        "for 2025-26 to support expansion [3]"
    )

    print_references([
        (
            "Women's Budget Group - Childcare Funding Gap "
            "(£5.2bn shortfall)",
            "https://wbg.org.uk/analysis/"
            "the-childcare-funding-gap/",
        ),
        (
            "NAO - DfE Overview 2024-25 "
            "(£6.2bn outturn, £8.2bn forecast)",
            "https://www.nao.org.uk/overviews/"
            "department-for-education-2024-25/",
        ),
        (
            "DfE - Early Years Funding 2025-26 "
            "Operational Guide",
            "https://www.gov.uk/government/publications/"
            "early-years-funding-2025-to-2026",
        ),
        (
            "IFS - Annual Report on Education Spending "
            "(Early Years Chapter)",
            "https://ifs.org.uk/publications/"
            "annual-report-education-spending-england-2025-26",
        ),
        (
            "Ceeda/DfE - Provider Cost Study 2024",
            "https://www.gov.uk/government/publications/"
            "early-years-provider-cost-study-2024",
        ),
    ])

    return rows


def main():
    args = parse_args("Increase DfE funding rates")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
