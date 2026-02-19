"""Baseline childcare spending analysis."""

from .utils import get_baseline, parse_args, fmt, row, print_references, reform_sim

ANALYSIS = "baseline"


def _uc_childcare_net_cost(sim_with_cc, sim_without_cc, year):
    """Net UC cost of childcare = UC(cc=on) - UC(cc=off).

    The childcare element is a pre-taper component of UC maximum amount.
    After the 55% earnings taper, the actual government spend is less
    than the gross element.  Differencing total UC payments gives the
    true fiscal cost.
    """
    uc_with = float(sim_with_cc.calculate("universal_credit", year).sum())
    uc_without = float(
        sim_without_cc.calculate("universal_credit", year).sum()
    )
    return uc_with - uc_without


def run(baseline, year):
    y = str(year)

    # Build a "no UC childcare" counterfactual (coverage_rate = 0)
    no_uc_cc = reform_sim({
        "gov.dwp.universal_credit.elements.childcare"
        ".coverage_rate": {y: 0.0},
    })

    variables = {
        "Tax-Free Childcare": "tax_free_childcare",
        "UC Childcare Element (net UC cost)": None,  # special
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
        if var is None:
            # UC childcare: net cost via differencing
            val = _uc_childcare_net_cost(baseline, no_uc_cc, year)
            var_name = "uc_childcare_element"
            gross = float(
                baseline.calculate("uc_childcare_element", year).sum()
            )
            print(
                f"  {label:55s} {fmt(val, 'bn'):>12s}"
                f"  (gross element: {fmt(gross, 'bn')})"
            )
        else:
            val = float(baseline.calculate(var, year).sum())
            var_name = var
            print(f"  {label:55s} {fmt(val, 'bn'):>12s}")
        total += val
        rows.append(row(ANALYSIS, "baseline", var_name, val))

    print(f"  {'TOTAL':55s} {fmt(total, 'bn'):>12s}")
    rows.append(row(ANALYSIS, "baseline", "total", total))

    # ── Like-for-like: run at external benchmark years ──────
    externals = {
        2025: {
            "label": "IFS 2025-26",
            "total": 10.5e9,
            "tfc": 632e6,
        },
        2024: {
            "label": "IFS/HMRC 2024-25",
            "total": 8.4e9,
            "tfc": 632e6,
        },
    }

    for lfl_year, ext in externals.items():
        lfl_y = str(lfl_year)
        lfl_no_uc_cc = reform_sim({
            "gov.dwp.universal_credit.elements.childcare"
            ".coverage_rate": {lfl_y: 0.0},
        })
        print(f"\n  ── Like-for-like: PE at year {lfl_year} "
              f"({ext['label']}) ──")
        lfl_total = 0
        for label, var in variables.items():
            if var is None:
                val = _uc_childcare_net_cost(
                    baseline, lfl_no_uc_cc, lfl_year
                )
                var_name = "uc_childcare_element"
            else:
                val = float(baseline.calculate(var, lfl_year).sum())
                var_name = var
            lfl_total += val
            print(f"    {label:55s} {fmt(val, 'bn'):>12s}")
            rows.append(
                row(ANALYSIS, f"baseline_{lfl_year}", var_name,
                    val, year=lfl_year)
            )
        print(f"    {'TOTAL':55s} {fmt(lfl_total, 'bn'):>12s}")
        print(f"    External total ({ext['label']}): "
              f"{fmt(ext['total'], 'bn')}")
        rows.append(
            row(ANALYSIS, f"baseline_{lfl_year}", "total",
                lfl_total, year=lfl_year)
        )
        rows.append(
            row(ANALYSIS, f"baseline_{lfl_year}", "external_total",
                ext["total"], year=lfl_year)
        )

    print(f"\n  PE baseline total ({year}): {fmt(total, 'bn')}")

    print("\n  Official spending (latest verified):")
    print("    TFC:        HMRC £632m in 2024-25 (826k families) [2]")
    print("    UC CC:      DWP ~£850m annualised (160k HHs × £420/mo, Aug 2025) [4]")
    print("    DfE total:  NAO £6.2bn outturn 2024-25, £8.2bn forecast 2025-26 [7]")

    print("\n  Other external estimates:")
    print(
        "    IFS: Total public childcare spending "
        "£8.4bn 2024-25, ~£10.5bn 2025-26 [5]"
    )
    print(
        "    IFS: Free entitlement spending "
        "£8.7bn in 2025-26 [5]"
    )
    print(
        "    OBR: 2023 childcare expansion alone "
        "~£3.3bn in 2025-26, £4.1bn by 2027-28 [6]"
    )

    print_references([
        (
            "PolicyEngine - Childcare Programmes in "
            "PolicyEngine UK (June 2025)",
            "https://www.policyengine.org/uk/research/"
            "uk-childcare-report",
        ),
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
            "DWP - UC Childcare Element Statistics "
            "to August 2025 (160k HHs, £420/mo avg)",
            "https://www.gov.uk/government/statistics/"
            "universal-credit-statistics-29-april-2013-"
            "to-9-october-2025",
        ),
        (
            "IFS - Annual Report on Education Spending "
            "in England 2025-26 (£8.7bn free entitlements)",
            "https://ifs.org.uk/publications/"
            "annual-report-education-spending-"
            "england-2025-26",
        ),
        (
            "OBR - Spring Budget 2023 Childcare "
            "Expansion Costing (£3.3bn 2025-26)",
            "https://obr.uk/docs/dlm_uploads/"
            "Annexes-March-2023.pdf",
        ),
        (
            "NAO - DfE Overview 2024-25 "
            "(£6.2bn outturn, £8.2bn forecast 2025-26)",
            "https://www.nao.org.uk/overviews/"
            "department-for-education-2024-25/",
        ),
    ])

    return rows


def main():
    args = parse_args("Baseline childcare spending")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
