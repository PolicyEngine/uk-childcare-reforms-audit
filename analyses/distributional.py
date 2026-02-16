"""Distributional analysis of a combined childcare reform package."""

import numpy as np
from .utils import (
    get_baseline,
    parse_args,
    reform_sim,
    fmt,
    row,
    CURRENCY,
    print_references,
)

ANALYSIS = "distributional"


def run(baseline, year):
    y = str(year)

    reform_params = {
        "gov.dwp.universal_credit.elements.childcare"
        ".coverage_rate": {y: 1.0},
        "gov.dwp.universal_credit.elements.childcare"
        ".cap.1": {y: 2063.76},
        "gov.dwp.universal_credit.elements.childcare"
        ".cap.2": {y: 3537.88},
        "gov.dfe.extended_childcare_entitlement"
        ".hours[1].amount": {y: 30},
        "gov.dfe.extended_childcare_entitlement"
        ".hours[2].amount": {y: 30},
    }

    sim = reform_sim(reform_params)

    baseline_income = baseline.calculate(
        "household_net_income", year
    )
    reform_income = sim.calculate(
        "household_net_income", year
    )
    weights = baseline.calculate(
        "household_weight", year, unweighted=True
    )
    equiv_income = baseline.calculate(
        "equiv_household_net_income", year
    )

    gain = np.array(reform_income) - np.array(baseline_income)
    equiv_vals = np.array(equiv_income)
    weight_vals = np.array(weights)

    decile_boundaries = np.percentile(
        equiv_vals, np.arange(10, 100, 10)
    )

    print("  Reform: UC 100% + double caps + 30hrs all 1-4")
    print(
        f"  {'Decile':>8s}  {'Total gain':>14s}"
        f"  {'Avg gain/hh':>14s}"
    )

    rows = []
    total_gain = 0
    for i in range(10):
        if i == 0:
            mask = equiv_vals <= decile_boundaries[0]
        elif i == 9:
            mask = equiv_vals > decile_boundaries[8]
        else:
            mask = (
                equiv_vals > decile_boundaries[i - 1]
            ) & (equiv_vals <= decile_boundaries[i])
        decile_gain = float(
            (gain[mask] * weight_vals[mask]).sum()
        )
        decile_count = float(weight_vals[mask].sum())
        avg = decile_gain / decile_count if decile_count else 0
        total_gain += decile_gain
        print(
            f"  {i+1:8d}  {fmt(decile_gain, 'm'):>14s}  "
            f"{CURRENCY}{avg:>10,.0f}"
        )
        rows.append(
            row(ANALYSIS, f"decile_{i+1}",
                "total_gain", decile_gain)
        )
        rows.append(
            row(ANALYSIS, f"decile_{i+1}",
                "avg_gain_per_hh", avg)
        )

    print(f"  {'Total':>8s}  {fmt(total_gain, 'bn'):>14s}")
    rows.append(
        row(ANALYSIS, "all", "total_gain", total_gain)
    )

    print("\n  External comparison:")
    print(
        "    IPPR: Largest gains to lowest-income "
        "households [1]"
    )
    print(
        "    Res Foundation: Part-time cleaners lose "
        "£7/wk vs not working [2]"
    )
    print(
        "    IFS: Higher earners benefit more from TFC "
        "than UC families [3]"
    )

    print_references([
        (
            "IPPR - A Childcare Guarantee "
            "(distributional analysis)",
            "https://www.ippr.org/articles/"
            "a-childcare-guarantee",
        ),
        (
            "Resolution Foundation - Costly Childcare "
            "(distributional impact)",
            "https://www.resolutionfoundation.org/publications/"
            "costly-childcare/",
        ),
        (
            "IFS - The health of the early years sector "
            "(distributional data)",
            "https://ifs.org.uk/publications/"
            "health-early-years-sector",
        ),
    ])

    return rows


def main():
    args = parse_args("Distributional analysis")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
