"""Analysis: IFS revised entitlement cost forecast (baseline validation)."""

from .utils import (
    get_baseline,
    parse_args,
    fmt,
    row,
    print_references,
)

ANALYSIS = "ifs_entitlement_forecast"


def run(baseline, year):
    print("  IFS: New entitlements could cost £5.0-5.3bn by 2028-29")
    print("  Comparing PE extended entitlement baseline against IFS forecast")

    # Calculate PE's extended entitlement for 2026 and 2028
    rows = []
    for check_year in [year, 2028]:
        val = float(
            baseline.calculate(
                "extended_childcare_entitlement", check_year
            ).sum()
        )
        print(f"    PE extended entitlement ({check_year}): "
              f"{fmt(val, 'bn')}")
        rows.append(
            row(ANALYSIS, f"PE baseline ({check_year})",
                "extended_childcare_entitlement",
                val, year=check_year)
        )

    # Record IFS forecast
    rows.append(
        row(ANALYSIS, "IFS forecast (2028-29)",
            "external_low", 5.0e9, year=2028)
    )
    rows.append(
        row(ANALYSIS, "IFS forecast (2028-29)",
            "external_high", 5.3e9, year=2028)
    )

    print("\n  External comparison:")
    print("    IFS: £5.0-5.3bn by 2028-29 [1]")

    print_references([
        (
            "IFS - Popularity of new childcare entitlements "
            "could leave spending much higher than forecast "
            "(£5.0-5.3bn by 2028-29)",
            "https://ifs.org.uk/articles/"
            "popularity-new-childcare-entitlements-"
            "could-leave-spending-much-higher-"
            "initially-forecast",
        ),
    ])

    return rows


def main():
    args = parse_args("IFS entitlement forecast comparison")
    run(get_baseline(), args.year)


if __name__ == "__main__":
    main()
