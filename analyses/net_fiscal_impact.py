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

    # Record external benchmarks for each bundle
    externals = {
        "UC 100% coverage + double caps": 150e6,
        "30hrs all 1-4yrs + 48 weeks": 2.1e9,
        "Double funding rates": 5.2e9,
    }
    for bundle_name, ext_val in externals.items():
        rows.append(
            row(ANALYSIS, bundle_name, "external", ext_val)
        )

    print("\n  External comparison:")
    print(
        "    IFS: 2023 expansion overspent by ~£440m "
        "(28%) in 2024-25; ~£1bn higher from 2026 [1]"
    )
    print(
        "    IFS: Spending Review added £1.6bn top-up "
        "for 2025-26 to 2028-29 [1]"
    )
    print(
        "    IPPR universal guarantee: £17.8bn gross, "
        "£9.7bn net (offset by £8bn employment gains) [2]"
    )
    print(
        "    Himmelweit/Sevilla: £7.3-17.9bn net "
        "(depending on scope) [3]"
    )
    print(
        "    Res Foundation 25hrs/47wks for 3-4yr: "
        "~£2.1bn [4]"
    )
    print(
        "    CPAG: 85%->100% UC coverage costs "
        "£150m initially [6]"
    )

    print_references([
        (
            "IFS - Annual Report on Education Spending "
            "in England 2025-26 (£440m overspend, "
            "£1.6bn top-up)",
            "https://ifs.org.uk/publications/"
            "annual-report-education-spending-england-2025-26",
        ),
        (
            "IPPR / Save the Children - A Childcare "
            "Guarantee (£17.8bn gross, £9.7bn net)",
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
            "Resolution Foundation - An Equal Start "
            "(25hrs/47wks = £2.1bn)",
            "https://www.resolutionfoundation.org/publications/"
            "an-equal-start/",
        ),
        (
            "OBR - Spring Budget 2023 Policy Costings",
            "https://obr.uk/docs/dlm_uploads/"
            "Annexes-March-2023.pdf",
        ),
        (
            "CPAG - Universal Credit: A Three-Step Plan "
            "(85%->100% = £150m)",
            "https://cpag.org.uk/news/"
            "universal-credit-three-step-plan",
        ),
    ])

    return rows


def main():
    args = parse_args("Net fiscal impact of combined reforms")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
