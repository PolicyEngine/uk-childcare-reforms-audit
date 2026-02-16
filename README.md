# UK Childcare Reforms Benchmark

**Live dashboard:** [uk-childcare-reforms-benchmark.vercel.app](https://uk-childcare-reforms-benchmark.vercel.app)

This project uses the [PolicyEngine UK](https://www.policyengine.org/uk) microsimulation model to stress-test childcare subsidy reforms for the 2026 tax year. Each analysis models a specific policy lever, compares the results against official government estimates and external benchmarks from the IFS, IPPR, Resolution Foundation, the Women's Budget Group, and the OBR, and reports the fiscal cost of each reform.

See the [PolicyEngine UK childcare report](https://www.policyengine.org/uk/research/uk-childcare-report) for full methodology.

## Dashboard

The interactive dashboard is a static React app built with [Vite](https://vitejs.dev/), [Recharts](https://recharts.org/), and [PapaParse](https://www.papaparse.com/). It visualises all 158 data points from 14 analyses.

```bash
cd dashboard
npm install
npm run dev       # Local dev server
npm run build     # Production build (output: dist/)
```

Deployed automatically to Vercel from the `dashboard/` directory.

## Analyses

The CLI runner executes 14 microsimulation analyses and outputs results to CSV.

### Setup

```bash
pip install -r requirements.txt
```

### Usage

```bash
python run.py --list                   # List available analyses
python run.py baseline                 # Run baseline (default year: 2026)
python run.py uc_coverage --year 2025  # Run one analysis for a specific year
python run.py uc_caps uc_coverage      # Run multiple analyses
python run.py all                      # Run everything
```

Results are saved to `output/results_{year}.csv`.

### Available analyses

| Key | Description |
|-----|-------------|
| `baseline` | Baseline childcare spending across all seven programmes |
| `takeup` | Take-up sensitivity (25%–100%) for TFC, extended, universal, and targeted entitlements |
| `uc_caps` | UC childcare caps (+50%, double) |
| `uc_coverage` | UC coverage rate (85% to 100%) |
| `extended_hours` | Extended hours (30/40 hours for all ages 1–4) |
| `tfc_rate` | TFC government top-up rate (20% to 50%) |
| `tfc_caps` | TFC annual caps (£3k/£6k, £4k/£8k) |
| `income_cap` | Income cap for TFC and extended entitlement (£100k to uncapped) |
| `funding_rates` | DfE provider funding rates (+20%, +50%, double) |
| `targeted` | Targeted entitlement income thresholds (£20k–£30k) |
| `weeks` | Funded weeks per year (38 to 52) |
| `min_hours` | Minimum work hours requirement (16 to 1 hour per week) |
| `fiscal` | Net fiscal impact of four composite reform packages |
| `distributional` | Distributional analysis by income decile |

## Childcare programmes in PolicyEngine UK

| Programme | Department | Description |
|-----------|------------|-------------|
| Tax-Free Childcare (TFC) | HMRC | 20% government top-up, up to £2,000 per child per year |
| UC childcare element | DWP | 85% of costs, up to £1,014.63/month (one child) or £1,739.37 (two or more) |
| WTC childcare element | DWP | Legacy tax credit childcare support |
| Universal entitlement | DfE | 15 hours per week for all three- and four-year-olds |
| Targeted entitlement | DfE | 15 hours per week for eligible two-year-olds (means-tested) |
| Extended entitlement | DfE | 30 hours per week for working parents (ages 9 months to 4 years) |
| Care to Learn | DfE | Childcare support for young parents in education |

## Key references

- [PolicyEngine UK childcare report (June 2025)](https://www.policyengine.org/uk/research/uk-childcare-report)
- [IFS – Annual report on education spending in England 2025–26](https://ifs.org.uk/publications/annual-report-education-spending-england-2025-26)
- [OBR – Spring Budget 2023 policy costings](https://obr.uk/docs/dlm_uploads/Annexes-March-2023.pdf)
- [IPPR – A childcare guarantee (2024)](https://www.ippr.org/articles/a-childcare-guarantee)
- [Resolution Foundation – Costly childcare (2023)](https://www.resolutionfoundation.org/publications/costly-childcare/)
- [Women's Budget Group – The childcare funding gap](https://wbg.org.uk/analysis/the-childcare-funding-gap/)
- [HMRC – Tax-Free Childcare statistics (September 2025)](https://www.gov.uk/government/statistics/tax-free-childcare-statistics-september-2025)
- [DfE – Education provision: children under 5](https://explore-education-statistics.service.gov.uk/find-statistics/education-provision-children-under-5)
- [DWP – UC statistics (Stat-Xplore)](https://stat-xplore.dwp.gov.uk/)
- [Coram – Childcare survey 2024](https://www.coram.org.uk/resource/childcare-survey-2024)

## Repository structure

```
uk-childcare-reforms-audit/
├── run.py                          # CLI entry point
├── requirements.txt
├── README.md
├── analyses/
│   ├── __init__.py
│   ├── utils.py                    # Shared utilities
│   ├── baseline.py
│   ├── takeup_sensitivity.py
│   ├── uc_coverage.py
│   ├── uc_caps.py
│   ├── extended_hours.py
│   ├── tfc_rate.py
│   ├── tfc_caps.py
│   ├── income_cap.py
│   ├── funding_rates.py
│   ├── targeted_eligibility.py
│   ├── extend_weeks.py
│   ├── min_work_hours.py
│   ├── net_fiscal_impact.py
│   └── distributional.py
└── dashboard/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── public/
    │   └── results.csv             # Pre-computed simulation output
    └── src/
        ├── main.jsx
        ├── App.jsx                 # Dashboard UI
        └── index.css
```
