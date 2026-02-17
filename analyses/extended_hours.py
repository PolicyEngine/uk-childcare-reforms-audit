"""Analysis: Expand extended childcare hours."""

from .utils import (
    get_baseline,
    parse_args,
    run_scenarios,
    reform_sim,
    fmt,
    row,
    print_references,
)

ANALYSIS = "extended_hours"


def run(baseline, year):
    y = str(year)
    print("  Government 2023 expansion phases in 30hrs for ages 9m-4")
    print("  IPPR proposes wrap-around care up to 40+ hrs")

    results = run_scenarios(
        {
            "Baseline (current phased)": {},
            "30hrs all ages 1-4 (full rollout)": {
                "gov.dfe.extended_childcare_entitlement"
                ".hours[1].amount": {y: 30},
                "gov.dfe.extended_childcare_entitlement"
                ".hours[2].amount": {y: 30},
            },
            "40hrs all ages 1-4 (IPPR wrap-around)": {
                "gov.dfe.extended_childcare_entitlement"
                ".hours[1].amount": {y: 40},
                "gov.dfe.extended_childcare_entitlement"
                ".hours[2].amount": {y: 40},
                "gov.dfe.extended_childcare_entitlement"
                ".hours[3].amount": {y: 40},
                "gov.dfe.extended_childcare_entitlement"
                ".hours[4].amount": {y: 40},
            },
        },
        [("ECE", "extended_childcare_entitlement")],
        baseline,
        year,
    )

    rows = []
    base = results["Baseline (current phased)"]["Combined"]
    for sc, totals in results.items():
        rows.append(
            row(ANALYSIS, sc,
                "extended_childcare_entitlement",
                totals["Combined"])
        )
        if sc != "Baseline (current phased)":
            rows.append(
                row(ANALYSIS, sc, "delta",
                    totals["Combined"] - base)
            )

    # ── Like-for-like: OBR 2023 expansion ─────────────────
    # OBR costed the expansion (extending 30hrs to under-3s)
    # at £3.3bn for 2025-26, rising to £4.1bn by 2027-28.
    # We create a "pre-expansion" sim (hours[1] & hours[2] = 0
    # for younger ages) and compare to PE baseline at the
    # same year.
    for lfl_year, ext_val, ext_label in [
        (2025, 3.3e9, "OBR 2025-26"),
        (2027, 4.1e9, "OBR 2027-28"),
    ]:
        lfl_y = str(lfl_year)
        pre_exp_sim = reform_sim({
            "gov.dfe.extended_childcare_entitlement"
            ".hours[1].amount": {lfl_y: 0},
            "gov.dfe.extended_childcare_entitlement"
            ".hours[2].amount": {lfl_y: 0},
        })
        pre_val = float(
            pre_exp_sim.calculate(
                "extended_childcare_entitlement", lfl_year
            ).sum()
        )
        post_val = float(
            baseline.calculate(
                "extended_childcare_entitlement", lfl_year
            ).sum()
        )
        lfl_delta = post_val - pre_val
        label = f"OBR expansion like-for-like ({lfl_year})"
        print(f"\n  ── Like-for-like: {ext_label} ──")
        print(f"    PE  (expansion cost, {lfl_year}): "
              f"{fmt(lfl_delta, 'bn')}")
        print(f"    OBR estimate ({ext_label}): "
              f"{fmt(ext_val, 'bn')}")
        rows.append(
            row(ANALYSIS, label, "delta",
                lfl_delta, year=lfl_year)
        )
        rows.append(
            row(ANALYSIS, label, "external",
                ext_val, year=lfl_year)
        )

    # Also add DfE phased costing comparison
    for lfl_year, ext_val, ext_label in [
        (2024, 1.7e9, "DfE 2024-25"),
        (2025, 3.3e9, "DfE 2025-26"),
        (2026, 4.1e9, "DfE 2026-27"),
    ]:
        lfl_y = str(lfl_year)
        pre_exp_sim = reform_sim({
            "gov.dfe.extended_childcare_entitlement"
            ".hours[1].amount": {lfl_y: 0},
            "gov.dfe.extended_childcare_entitlement"
            ".hours[2].amount": {lfl_y: 0},
        })
        pre_val = float(
            pre_exp_sim.calculate(
                "extended_childcare_entitlement", lfl_year
            ).sum()
        )
        post_val = float(
            baseline.calculate(
                "extended_childcare_entitlement", lfl_year
            ).sum()
        )
        lfl_delta = post_val - pre_val
        label = f"DfE expansion like-for-like ({lfl_year})"
        print(f"    PE  (DfE expansion, {lfl_year}): "
              f"{fmt(lfl_delta, 'bn')}")
        print(f"    DfE estimate ({ext_label}): "
              f"{fmt(ext_val, 'bn')}")
        rows.append(
            row(ANALYSIS, label, "delta",
                lfl_delta, year=lfl_year)
        )
        rows.append(
            row(ANALYSIS, label, "external",
                ext_val, year=lfl_year)
        )

    print("\n  External comparison:")
    print(
        "    OBR: 2023 expansion costs £3.3bn in 2025-26, "
        "£4.1bn by 2027-28 [1]"
    )
    print(
        "    IFS: Take-up 26% higher than Dec 2023 "
        "projections; overspend of ~£440m (28%) "
        "in 2024-25 [2]"
    )
    print(
        "    IFS: Spending could end up ~£1bn higher "
        "than forecast from 2026 onwards [2]"
    )
    print("    IPPR wrap-around (0-11): £17.8bn gross [3]")
    print(
        "    DfE: Expansion cost £1.7bn 2024-25, "
        "£3.3bn 2025-26, £4.1bn 2026-27 [4]"
    )
    print(
        "\n  NOTE: 30hrs and 40hrs may give identical results "
        "because maximum_extended_childcare_hours_usage "
        "defaults to 30 hrs/week."
    )

    print_references([
        (
            "OBR - Spring Budget 2023 Policy Costings "
            "(£3.3bn 2025-26, £4.1bn 2027-28)",
            "https://obr.uk/docs/dlm_uploads/"
            "Annexes-March-2023.pdf",
        ),
        (
            "IFS - Popularity of new childcare entitlements "
            "(26% over projection, £440m overspend, "
            "~£1bn higher from 2026)",
            "https://ifs.org.uk/articles/"
            "popularity-new-childcare-entitlements-"
            "could-leave-spending-much-higher-"
            "initially-forecast",
        ),
        (
            "IPPR - A Childcare Guarantee (wrap-around "
            "£17.8bn gross)",
            "https://www.ippr.org/articles/"
            "a-childcare-guarantee",
        ),
        (
            "DfE - Spring Budget 2023 Childcare Expansion "
            "Costing Note (£1.7bn, £3.3bn, £4.1bn)",
            "https://assets.publishing.service.gov.uk/"
            "media/66221ba8252f0d71cf757d2b/"
            "Spring_budget_2023_childcare_expansion_"
            "costing_note_information.pdf",
        ),
    ])

    return rows


def main():
    args = parse_args("Expand extended childcare hours")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
