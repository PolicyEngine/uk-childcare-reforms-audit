"""Baseline childcare spending analysis."""

from .utils import get_baseline, parse_args, fmt, row, print_references

ANALYSIS = "baseline"


def run(baseline, year):
    variables = {
        "Tax-Free Childcare": "tax_free_childcare",
        "UC Childcare Element": "uc_childcare_element",
        "WTC Childcare Element": "WTC_childcare_element",
        "Universal Childcare Entitlement (15hrs, 3-5)": (
            "universal_childcare_entitlement"
        ),
        "Targeted Childcare Entitlement (15hrs, age 2)": (
            "targeted_childcare_entitlement"
        ),
        "Extended Childcare Entitlement (30hrs, work-cond)": (
            "extended_childcare_entitlement"
        ),
        "Care to Learn (under-20 parents in education)": (
            "care_to_learn"
        ),
    }

    rows = []
    total = 0
    for label, var in variables.items():
        val = float(baseline.calculate(var, year).sum())
        total += val
        print(f"  {label:55s} {fmt(val, 'bn'):>12s}")
        rows.append(row(ANALYSIS, "baseline", var, val))

    print(f"  {'TOTAL':55s} {fmt(total, 'bn'):>12s}")
    rows.append(row(ANALYSIS, "baseline", "total", total))

    print("\n  PE childcare report comparison (2025 estimates):")
    print("    TFC:        PE report £0.7bn [1]")
    print("    Extended:   PE report £4.4bn [1]")
    print("    Universal:  PE report £1.8bn [1]")
    print("    Targeted:   PE report £0.5bn [1]")

    print("\n  Government-reported spending (2024):")
    print("    TFC:        Gov £0.6bn [2]")
    print("    Extended:   Gov £2.5bn [3]")
    print("    Universal:  Gov £1.7bn [3]")
    print("    Targeted:   Gov £0.6bn [3]")
    print("    UC CC:      DWP ~£1.0bn in 2023-24 [4]")

    print("\n  Other external estimates:")
    print(
        "    IFS: Total early years spending "
        "~£8.7bn in 2025-26 [5]"
    )
    print(
        "    OBR: 2023 childcare expansion alone "
        "~£3.3bn in 2025-26 [6]"
    )
    print(f"    PE baseline total ({year}): {fmt(total, 'bn')}")

    print_references([
        (
            "PolicyEngine - Childcare Programmes in "
            "PolicyEngine UK (June 2025)",
            "https://www.policyengine.org/uk/research/"
            "uk-childcare-report",
        ),
        (
            "HMRC - Tax-Free Childcare Statistics "
            "September 2025",
            "https://www.gov.uk/government/statistics/"
            "tax-free-childcare-statistics-september-2025",
        ),
        (
            "DfE - Funded Early Education and Childcare "
            "2024",
            "https://explore-education-statistics"
            ".service.gov.uk/find-statistics/"
            "funded-early-education-and-childcare/2024",
        ),
        (
            "DWP - Universal Credit Statistics "
            "(childcare costs via Stat-Xplore)",
            "https://stat-xplore.dwp.gov.uk/",
        ),
        (
            "IFS - Annual Report on Education Spending "
            "in England 2025-26",
            "https://ifs.org.uk/publications/"
            "annual-report-education-spending-"
            "england-2025-26",
        ),
        (
            "OBR - Spring Budget 2023 Childcare "
            "Expansion Costing",
            "https://obr.uk/docs/dlm_uploads/"
            "Annexes-March-2023.pdf",
        ),
        (
            "DfE - Education Provision: Children Under 5 "
            "(funded entitlements)",
            "https://explore-education-statistics"
            ".service.gov.uk/find-statistics/"
            "education-provision-children-under-5",
        ),
    ])

    return rows


def main():
    args = parse_args("Baseline childcare spending")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
