"""Analysis: IFS compensate providers for min wage rises since 2017."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    fmt,
    row,
    print_references,
)

ANALYSIS = "ifs_min_wage_comp"


def run(baseline, year):
    y = str(year)
    # Min wage rose from £7.50 (2017) to £11.44 (2024) = +52.5%
    # ~70% of provider costs are staffing
    # IFS estimates £685m to compensate
    # Approximate as ~18% increase in all funding rates
    # (52.5% wage rise * 70% cost share * partial pass-through)
    pct_increase = 0.18
    base_rates = [11.54, 8.53, 6.12]
    new_rates = [round(r * (1 + pct_increase), 2) for r in base_rates]

    print("  IFS: Min wage rose £7.50 to £11.44 since 2017 (+52.5%)")
    print("  ~70% of provider costs are staffing")
    print(f"  Approximate as ~{pct_increase*100:.0f}% funding rate increase")
    print(f"  New rates: <2: £{new_rates[0]}/hr, "
          f"2: £{new_rates[1]}/hr, 3+: £{new_rates[2]}/hr")

    results = run_scenarios(
        {
            "Baseline (DfE 2025-26 rates)": {},
            "IFS min wage compensation (+18%)": {
                "gov.dfe.childcare_funding_rate[0].amount": {
                    y: new_rates[0]
                },
                "gov.dfe.childcare_funding_rate[1].amount": {
                    y: new_rates[1]
                },
                "gov.dfe.childcare_funding_rate[2].amount": {
                    y: new_rates[2]
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
    base = results["Baseline (DfE 2025-26 rates)"]["Combined"]
    for sc, totals in results.items():
        for label in ["UCE", "TCE", "ECE", "Combined"]:
            rows.append(
                row(ANALYSIS, sc, label, totals[label])
            )
        if sc != "Baseline (DfE 2025-26 rates)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    print("\n  External comparison:")
    print("    IFS: £685m to compensate providers [1]")

    print_references([
        (
            "IFS - Complicated, costly and constantly "
            "changing (£685m min wage compensation)",
            "https://ifs.org.uk/articles/"
            "complicated-costly-and-constantly-changing-"
            "childcare-system-england",
        ),
    ])

    return rows


def main():
    args = parse_args("IFS min wage compensation")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
