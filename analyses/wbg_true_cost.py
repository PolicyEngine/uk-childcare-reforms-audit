"""Analysis: WBG fund providers at true cost by age band."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    fmt,
    row,
    print_references,
)

ANALYSIS = "wbg_true_cost"


def run(baseline, year):
    y = str(year)
    print("  WBG 2024 updated analysis: true cost rates")
    print("  Under-2s: £17.48/hr (current £11.54)")
    print("  Age 2: £13.19/hr (current £8.53)")
    print("  Age 3+: £9.42/hr (current £6.12)")

    results = run_scenarios(
        {
            "Baseline (DfE 2025-26 rates)": {},
            "WBG true cost rates": {
                "gov.dfe.childcare_funding_rate[0].amount": {
                    y: 17.48
                },
                "gov.dfe.childcare_funding_rate[1].amount": {
                    y: 13.19
                },
                "gov.dfe.childcare_funding_rate[2].amount": {
                    y: 9.42
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
    print("    WBG: Additional £5bn needed in 2025/26 [1]")

    print_references([
        (
            "WBG - Updated analysis: early education and "
            "childcare funding shortfall (£5bn additional)",
            "https://www.wbg.org.uk/publication/"
            "updated-analysis-early-education-and-childcare/",
        ),
    ])

    return rows


def main():
    args = parse_args("WBG true cost rates")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
