"""Takeup sensitivity analysis for childcare schemes.

PolicyEngine calibrates take-up rates to match official spending and
caseload statistics. This analysis shows how total spending varies
across different assumed take-up levels, anchored by PE's calibrated
rates from the June 2025 childcare report (Table 9).
"""

from .utils import get_baseline, parse_args, fmt, row, print_references

ANALYSIS = "takeup"


def run(baseline, year):
    pe_calibrated = {
        "Tax-Free Childcare": 0.58,
        "Extended Childcare Entitlement": 0.81,
        "Universal Childcare Entitlement": 0.56,
        "Targeted Childcare Entitlement": 0.60,
    }

    var_names = {
        "Tax-Free Childcare": "tax_free_childcare",
        "Extended Childcare Entitlement": (
            "extended_childcare_entitlement"
        ),
        "Universal Childcare Entitlement": (
            "universal_childcare_entitlement"
        ),
        "Targeted Childcare Entitlement": (
            "targeted_childcare_entitlement"
        ),
    }

    sensitivity_rates = [0.25, 0.50, 0.75, 1.0]

    refs_text = {
        "Tax-Free Childcare": (
            "PE calibrated: 0.58; Gov: 660k children (2024)"
        ),
        "Extended Childcare Entitlement": (
            "PE calibrated: 0.81; Gov: 740k children (2024)"
        ),
        "Universal Childcare Entitlement": (
            "PE calibrated: 0.56; Gov: 490k children (2024)"
        ),
        "Targeted Childcare Entitlement": (
            "PE calibrated: 0.60; Gov: 130k children (2024)"
        ),
    }

    rows = []

    for name in pe_calibrated:
        var = var_names[name]
        cal_rate = pe_calibrated[name]
        print(f"\n  --- {name} ---")
        print(f"  Reference: {refs_text[name]}")
        full = float(baseline.calculate(var, year).sum())

        print(
            f"    PE calibrated ({cal_rate:.0%}): "
            f"{fmt(full, 'bn'):>12s}  <-- current model"
        )
        rows.append(
            row(ANALYSIS, name, f"calibrated_{cal_rate}", full)
        )

        for rate in sensitivity_rates:
            scaled = full * rate / cal_rate if cal_rate else 0
            marker = ""
            if abs(rate - cal_rate) < 0.02:
                marker = "  <-- ~calibrated"
            print(
                f"    If takeup {rate:5.0%}: "
                f"{fmt(scaled, 'bn'):>12s}{marker}"
            )
            rows.append(
                row(ANALYSIS, name, f"takeup_{rate}", scaled)
            )

    print("\n  Official spending comparison (latest verified):")
    print("    TFC:        HMRC £632m 2024-25 (826k families) [1]")
    print("    UC CC:      DWP ~£850m annualised (160k HHs, Aug 2025) [5]")
    print("    DfE total:  NAO £6.2bn outturn 2024-25 [6]")
    print("    IFS total:  £8.4bn all public childcare 2024-25 [7]")

    print("\n  Key takeup facts:")
    print(
        "    DWP: Only 13% of eligible UC families "
        "claim the childcare element [5]"
    )
    print(
        "    IFS: Only ~40% of eligible families "
        "aware of TFC [7]"
    )
    print(
        "    ~63% of children aged 0-4 use formal "
        "childcare (2023 DfE survey) [4]"
    )

    print("\n  PE calibration methodology:")
    print(
        "    Take-up rates are optimised to match "
        "official spending and caseload targets [3]"
    )
    print(
        "    Extended hours: imputed via N(15.0, 5.0) "
        "distribution, bounded (0, 40] [3]"
    )

    print_references([
        (
            "HMRC - Tax-Free Childcare Statistics "
            "September 2025 (£632m, 826k families)",
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
            "PolicyEngine - Childcare Programmes in "
            "PolicyEngine UK (June 2025, Tables 8-9)",
            "https://www.policyengine.org/uk/research/"
            "uk-childcare-report",
        ),
        (
            "DfE - Childcare and Early Years Survey of "
            "Parents 2023",
            "https://www.gov.uk/government/statistics/"
            "childcare-and-early-years-survey-of-"
            "parents-2023",
        ),
        (
            "DWP - UC Childcare Element Statistics "
            "to August 2025 (160k HHs, 13% takeup)",
            "https://www.gov.uk/government/statistics/"
            "universal-credit-statistics-29-april-2013-"
            "to-9-october-2025",
        ),
        (
            "NAO - DfE Overview 2024-25 "
            "(£6.2bn early years outturn)",
            "https://www.nao.org.uk/overviews/"
            "department-for-education-2024-25/",
        ),
        (
            "IFS - Annual Report on Education Spending "
            "2025-26 (£8.4bn total, £8.7bn entitlements)",
            "https://ifs.org.uk/publications/"
            "annual-report-education-spending-"
            "england-2025-26",
        ),
    ])

    return rows


def main():
    args = parse_args("Takeup sensitivity analysis")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
