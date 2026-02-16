"""Net fiscal impact of key combined childcare reforms."""

from .utils import (
    get_baseline,
    parse_args,
    reform_sim,
    fmt,
    row,
    print_references,
)

ANALYSIS = "fiscal"


def run(baseline, year):
    y = str(year)

    key_reforms = {
        "UC 100% coverage + double caps": {
            "gov.dwp.universal_credit.elements.childcare"
            ".coverage_rate": {y: 1.0},
            "gov.dwp.universal_credit.elements.childcare"
            ".cap.1": {y: 2063.76},
            "gov.dwp.universal_credit.elements.childcare"
            ".cap.2": {y: 3537.88},
        },
        "30hrs all 1-4yrs + 48 weeks": {
            "gov.dfe.extended_childcare_entitlement"
            ".hours[1].amount": {y: 30},
            "gov.dfe.extended_childcare_entitlement"
            ".hours[2].amount": {y: 30},
            "gov.dfe.weeks_per_year": {y: 48},
        },
        "Double funding rates": {
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
        "TFC 50% top-up + £4k cap": {
            "gov.hmrc.tax_free_childcare.contribution"
            ".rate": {y: 0.50},
            "gov.hmrc.tax_free_childcare.contribution"
            ".standard_child": {y: 4000},
        },
    }

    baseline_hh = float(
        baseline.calculate("household_net_income", year).sum()
    )

    rows = []
    for name, params in key_reforms.items():
        sim = reform_sim(params)
        reform_hh = float(
            sim.calculate("household_net_income", year).sum()
        )
        net_cost = reform_hh - baseline_hh
        print(
            f"  {name:45s} net cost: {fmt(net_cost, 'bn')}"
        )
        rows.append(row(ANALYSIS, name, "net_cost", net_cost))

    print("\n  External comparison:")
    print(
        "    IFS: 2023 expansion revised cost ~£1bn "
        "higher than forecast [1]"
    )
    print("    IPPR universal guarantee: £7.7bn net [2]")
    print(
        "    Himmelweit/Sevilla: £7.3-17.9bn net "
        "(depending on scope) [3]"
    )
    print(
        "    Res Foundation 25hrs/47wks for 3-4yr: "
        "~£2.1bn [4]"
    )

    print_references([
        (
            "IFS - Annual Report on Education Spending "
            "in England 2025-26",
            "https://ifs.org.uk/publications/"
            "annual-report-education-spending-england-2025-26",
        ),
        (
            "IPPR - A Childcare Guarantee "
            "(fiscal analysis)",
            "https://www.ippr.org/articles/"
            "a-childcare-guarantee",
        ),
        (
            "Himmelweit & Sevilla - Childcare as "
            "Infrastructure (academic paper)",
            "https://wbg.org.uk/analysis/"
            "a-new-approach-to-childcare/",
        ),
        (
            "Resolution Foundation - An Equal Start",
            "https://www.resolutionfoundation.org/publications/"
            "an-equal-start/",
        ),
        (
            "OBR - Spring Budget 2023 Policy Costings",
            "https://obr.uk/docs/dlm_uploads/"
            "Annexes-March-2023.pdf",
        ),
    ])

    return rows


def main():
    args = parse_args("Net fiscal impact of combined reforms")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
