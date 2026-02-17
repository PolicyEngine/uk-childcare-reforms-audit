import { useState, useEffect } from "react";
import Papa from "papaparse";

/* ── Formatting helpers ──────────────────────────────────── */

function fmt(v) {
  if (v == null) return "\u2014";
  const abs = Math.abs(v);
  if (abs >= 1e9) return `\u00A3${(v / 1e9).toFixed(2)}bn`;
  if (abs >= 1e6) return `\u00A3${(v / 1e6).toFixed(0)}m`;
  return `\u00A3${v.toLocaleString("en-GB", { maximumFractionDigits: 0 })}`;
}

function pct(pe, ext) {
  if (!pe || !ext) return null;
  return ((pe - ext) / ext * 100).toFixed(0);
}

function getMatch(pe, ext) {
  if (pe == null || ext == null) return "none";
  const r = Math.abs(pe / ext - 1);
  if (r <= 0.20) return "close";
  if (r <= 0.75) return "moderate";
  return "divergent";
}

const MATCH_LABELS = {
  close: "Close match",
  moderate: "Moderate gap",
  divergent: "Large gap",
  none: "PE only",
};

/* ── Comparison definitions ──────────────────────────────── */
/* All external values are hardcoded. PE values are looked up */
/* from the CSV using analysis + scenario + metric.           */

const COMPARISONS = [
  // ── EXTENDED ENTITLEMENT (total spending) ──
  {
    category: "Extended Entitlement",
    reform: "Total extended childcare entitlement spending (30 funded hours, working families, children 9m\u20134yrs)",
    context: "Baseline total cost of the fully rolled-out extended entitlement (30 funded hours, ages 9m\u20134, working families). PE models at 81% calibrated take-up for 2026.",
    pe: { analysis: "extended_hours", scenario: "Baseline (current phased)", metric: "extended_childcare_entitlement" },
    extValue: 4.06e9,
    extLabel: "DfE / OBR projected programme cost (2026\u201327)",
    sourceUrl: "https://assets.publishing.service.gov.uk/media/66221ba8252f0d71cf757d2b/Spring_budget_2023_childcare_expansion_costing_note_information.pdf",
    sourceRef: "Table 1, row \u2018Total cost\u2019, 2026\u201327 column (\u00a34,060m)",
    comparability: "similar",
    whyDiffer: "PE models 2026 total extended entitlement spending at calibrated 81% take-up. OBR/DfE projected \u00a34.06bn for 2026\u201327 (\u00a34.1bn for 2027\u201328). Close alignment validates PE\u2019s modelling of the 2023 expansion.",
  },

  // ── PROVIDER FUNDING RATES ──
  {
    category: "Provider Funding Rates",
    reform: "Increase DfE provider funding rates by 50% across all age bands",
    context: "Raise DfE hourly provider rates by 50% across all age bands (e.g. under-2s from \u00a311.54 to \u00a317.31/hr). Applies to universal, targeted, and extended entitlement hours.",
    pe: { analysis: "funding_rates", scenario: "+50% rates", metric: "Combined" },
    extValue: 9.4e9,
    extLabel: "Women\u2019s Budget Group \u2014 total providers need",
    sourceUrl: "https://www.wbg.org.uk/publication/wbg-finds-government-funding-for-early-education-and-childcare-falls-short-by-5-2bn/",
    sourceRef: "Summary paragraph: \u2018an additional \u00a35.2bn would need to be allocated (\u00a39.4bn in total)\u2019",
    comparability: "similar",
    whyDiffer: "WBG estimates providers need \u00a39.4bn total (current \u00a34.2bn + \u00a35.2bn gap). PE\u2019s +50% rates yields a combined total very close to this target. A ~40% rate increase would match WBG\u2019s recommendation exactly.",
  },

  // ── REFORM BUNDLES ──
  {
    category: "Reform Bundles",
    reform: "Double all DfE provider funding rates (net fiscal cost)",
    context: "Double all DfE hourly provider rates (e.g. under-2s from \u00a311.54 to \u00a323.08/hr). Net fiscal cost = total increase in household net income versus baseline.",
    pe: { analysis: "fiscal", scenario: "Double funding rates", metric: "net_cost" },
    extValue: 5.2e9,
    extLabel: "Women\u2019s Budget Group \u2014 funding gap",
    sourceUrl: "https://www.wbg.org.uk/publication/wbg-finds-government-funding-for-early-education-and-childcare-falls-short-by-5-2bn/",
    sourceRef: "Summary paragraph: \u2018falls short by \u00a35.2bn\u2019",
    comparability: "similar",
    whyDiffer: "WBG estimates a \u00a35.2bn funding gap (providers need \u00a39.4bn vs current \u00a34.2bn). PE costs a more extreme reform (doubling all rates), which naturally exceeds WBG\u2019s gap estimate. PE\u2019s +50% scenario delta is a closer comparator.",
  },
  {
    category: "Reform Bundles",
    reform: "30hrs for all 1\u20134yr-olds + 48 weeks per year (net fiscal cost)",
    context: "Bundle: extend funded weeks from 38 (term-time) to 48 per year, and ensure 30hrs available for all 1\u20134yr-olds. Baseline: 30hrs for 38 weeks/year.",
    pe: { analysis: "fiscal", scenario: "30hrs all 1-4yrs + 48 weeks", metric: "net_cost" },
    extValue: 2.1e9,
    extLabel: "Resolution Foundation \u2014 The Costs of Childcare (25hrs/47wks, 3\u20134yr-olds)",
    sourceUrl: "https://www.resolutionfoundation.org/publications/costs-childcare-housing-costs/",
    sourceRef: "Section 4, Table 2: \u2018Universal 25hrs/47wks\u2019 scenario, gross cost column",
    comparability: "similar",
    whyDiffer: "Res Foundation costs 25hrs/47wks for 3\u20134yr-olds only (2012 estimate). PE costs 30hrs/48wks for all entitled ages (broader scope). Despite broader scope, PE estimate is lower \u2014 possibly because Res Foundation includes wrap-around or holiday provision costs PE doesn\u2019t capture.",
  },
  {
    category: "Reform Bundles",
    reform: "UC 100% coverage + double caps (net fiscal cost)",
    context: "Bundle: raise UC coverage from 85% to 100% (no co-pay) and double monthly caps from \u00a31,015/\u00a31,739 to \u00a32,030/\u00a33,479. Baseline: 85% coverage with current caps.",
    pe: { analysis: "fiscal", scenario: "UC 100% coverage + double caps", metric: "net_cost" },
    extValue: 150e6,
    extLabel: "CPAG \u2014 UC: A Three-Step Plan (coverage only, current claimants)",
    sourceUrl: "https://cpag.org.uk/news/universal-credit-three-step-plan",
    sourceRef: "Linked PDF report, Section \u2018Step 2: Cover 100% of childcare costs\u2019, costing table",
    comparability: "similar",
    whyDiffer: "CPAG costs only the coverage increase (85%\u2192100%) for ~160k current claimants. PE bundles coverage AND cap doubling across the full eligible population. The gap reflects the UC childcare take-up problem (13% actual vs 100% eligible).",
  },

  // ── BASELINE SPENDING ──
  {
    category: "Baseline Spending",
    reform: "Tax-Free Childcare spending (PE 2026 vs HMRC 2024\u201325 actuals)",
    context: "Baseline TFC spending at current policy: 20% government top-up, \u00a32k/\u00a34k annual caps. PE calibrates to 58% take-up for 2026.",
    pe: { analysis: "baseline", scenario: "baseline", metric: "tax_free_childcare" },
    extValue: 632e6,
    extLabel: "HMRC TFC Statistics Sep 2025 (826k families)",
    sourceUrl: "https://www.gov.uk/government/news/826000-families-boost-finances-with-childcare-savings",
    sourceRef: "Opening paragraph: \u2018826,000 UK families shared \u00a3632.2 million in government top-ups\u2019",
    comparability: "like-for-like",
    whyDiffer: "PE calibrates TFC to 58% take-up for 2026. HMRC reports 2024\u201325 actuals for 826k families. Moderate gap likely due to PE\u2019s 2026 forecast year vs HMRC\u2019s 2024\u201325 actuals and calibration differences.",
  },
  {
    category: "Baseline Spending",
    reform: "Universal childcare entitlement (15hrs, all 3\u20134yr-olds)",
    context: "Baseline spending on universal 15hrs/week for all 3\u20134yr-olds (38 weeks/year). PE calibrates to 56% take-up for 2026.",
    pe: { analysis: "baseline", scenario: "baseline", metric: "universal_childcare_entitlement" },
    extValue: 2.6e9,
    extLabel: "DfE Early Years Funding Formulae 2024\u201325",
    sourceUrl: "https://www.gov.uk/government/publications/early-years-funding-2024-to-2025/2024-to-2025-early-years-national-funding-formulae-technical-note",
    sourceRef: "Section \u2018Universal entitlement for 3 and 4-year-olds\u2019: \u2018This will total \u00a32.6 billion in 2024 to 2025\u2019",
    comparability: "similar",
    whyDiffer: "PE calibrated to 56% take-up. DfE figure covers all funded 3\u20134yr places including some non-universal provision. PE\u2019s lower estimate reflects modelling only the universal 15hr entitlement.",
  },
  {
    category: "Baseline Spending",
    reform: "Total government childcare spending (PE 2026 vs IFS 2025\u201326)",
    context: "Baseline total across all seven childcare programmes (TFC, UC, WTC, universal, targeted, extended entitlement, Care to Learn) at current policy settings for 2026.",
    pe: { analysis: "baseline", scenario: "baseline", metric: "total" },
    extValue: 10.5e9,
    extLabel: "IFS Annual Report on Education Spending 2025\u201326",
    sourceUrl: "https://ifs.org.uk/publications/annual-report-education-spending-england-2025-26",
    sourceRef: "Section \u2018Childcare\u2019: \u2018childcare spending reached \u00a38.4bn in 2024\u201325 and will be around \u00a310.5bn in 2025\u201326\u2019",
    comparability: "similar",
    whyDiffer: "PE models full eligible population including UC childcare element at full eligibility (~\u00a38bn). DWP reports only ~160k actual UC CC claimants (13% take-up, \u00a3850m). Excluding UC CC, PE total (~\u00a37.8bn) closely aligns with IFS (\u00a38.7bn entitlements only).",
  },
  {
    category: "Baseline Spending",
    reform: "UC childcare element spending (PE 2026 vs DWP annualised actuals)",
    context: "Baseline UC childcare element spending at current policy: 85% coverage rate, \u00a31,015/\u00a31,739 monthly caps. PE models the full eligible population (vs ~13% actual take-up).",
    pe: { analysis: "baseline", scenario: "baseline", metric: "uc_childcare_element" },
    extValue: 958e6,
    extLabel: "DWP UC Statistics May 2025 (~190k households, \u00a3420/mo avg, annualised)",
    sourceUrl: "https://www.gov.uk/government/statistics/universal-credit-statistics-29-april-2013-to-9-october-2025",
    sourceRef: "Table: \u2018People on UC with Childcare costs\u2019, latest month. Annualised: 190k \u00d7 \u00a3420/mo \u00d7 12 \u2248 \u00a3958m",
    comparability: "similar",
    whyDiffer: "Largest single divergence. PE models the full FRS eligible population at 100% eligibility. DWP reports only ~190k households actually claiming (~16% of eligible). The gap is well-documented: UC childcare requires upfront payment before reimbursement, depressing take-up.",
  },

  // ── UC CHILDCARE CAPS ──
  {
    category: "UC Childcare Caps",
    reform: "Double UC childcare monthly caps (\u00a31,015\u2192\u00a32,030 / \u00a31,739\u2192\u00a33,479)",
    context: "Double UC monthly childcare caps from \u00a31,015/\u00a31,739 to \u00a32,030/\u00a33,479. Only ~3% of current claimants hit the cap.",
    pe: { analysis: "uc_caps", scenario: "Double caps", metric: "delta" },
    extValue: 80e6,
    extLabel: "HM Treasury \u2014 Spring Budget 2023 costings (\u00a360\u2013100m/yr)",
    sourceUrl: "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1142824/Costing_Document_-_Spring_Budget_2023.pdf",
    sourceRef: "Page 10, \u2018Childcare: increase UC caps\u2019 row, annual cost columns (\u00a360\u2013100m range across years)",
    extNote: "HMT costed a smaller uprating (\u00a3646\u2192\u00a3951), not full doubling",
    comparability: "similar",
    whyDiffer: "HMT\u2019s \u00a360\u2013100m/yr was for the 2023 specific uprating (smaller than doubling) and costed only current claimants. PE models full doubling across full eligible population. Only 3% of UC CC claimants hit the cap.",
  },

  // ── FUNDED WEEKS ──
  {
    category: "Funded Weeks per Year",
    reform: "Extend funded childcare from 38 to 48 weeks per year (IPPR-style)",
    context: "Extend funded childcare from 38 weeks/year (term-time) to 48 weeks, covering most school holidays. Hours unchanged (30hrs extended, 15hrs universal/targeted).",
    pe: { analysis: "extend_weeks", scenario: "48 weeks (IPPR)", metric: "delta" },
    extValue: 2.1e9,
    extLabel: "Resolution Foundation \u2014 The Costs of Childcare (25hrs/47wks, 3\u20134yr-olds only)",
    sourceUrl: "https://www.resolutionfoundation.org/publications/costs-childcare-housing-costs/",
    sourceRef: "Section 4, Table 2: \u2018Universal 25hrs/47wks\u2019 scenario, gross cost column",
    comparability: "similar",
    whyDiffer: "PE runs 48 weeks at 30hrs for all entitled ages (9m\u20134). Res Foundation modelled 25hrs/47wks for 3\u20134yr-olds only (2012 estimate). Despite PE\u2019s broader scope, PE costs less \u2014 Res Foundation may include additional wrap-around provision.",
  },

  // ── UC CHILDCARE COVERAGE ──
  {
    category: "UC Childcare Coverage",
    reform: "Raise UC childcare coverage rate from 85% to 100%",
    context: "Raise UC childcare reimbursement from 85% to 100% of costs, eliminating the 15% parental co-pay.",
    pe: { analysis: "uc_coverage", scenario: "100% coverage", metric: "delta" },
    extValue: 150e6,
    extLabel: "CPAG \u2014 UC: A Three-Step Plan (2024)",
    sourceUrl: "https://cpag.org.uk/news/universal-credit-three-step-plan",
    sourceRef: "Linked PDF report, Section \u2018Step 2: Cover 100% of childcare costs\u2019, costing table",
    comparability: "similar",
    whyDiffer: "CPAG\u2019s \u00a3150m covers only the ~160k households currently claiming UC childcare (13% of eligible). PE models the full FRS eligible population. The gap directly reflects the known UC childcare take-up problem, not a modelling error.",
  },

  // ── INCOME CAP ──
  {
    category: "Income Cap",
    reform: "Raise \u00a3100k income cap for TFC + extended entitlement to \u00a3150k",
    context: "Raise the \u00a3100k per-parent income cap for TFC and extended entitlement to \u00a3150k, removing the cliff-edge where families lose all support at \u00a3100,001.",
    pe: { analysis: "income_cap", scenario: "\u00a3150k cap", metric: "delta" },
    extValue: 1.4e9,
    extLabel: "Government estimate (via AJ Bell) for \u00a3120k\u2013\u00a3160k range",
    sourceUrl: "https://www.ajbell.co.uk/news/beat-ps100000-tax-trap-cost-could-cost-parents-tens-thousands",
    sourceRef: "Article body: \u2018The government said the reforms would eventually cost \u00a31.4 billion if the threshold were increased to \u00a3120,000\u2013\u00a3160,000\u2019",
    comparability: "similar",
    whyDiffer: "Govt\u2019s \u00a31.4bn estimate covers a \u00a3120k\u2013\u00a3160k per-parent range. PE\u2019s \u00a3150k scenario is within that range but costs much less. Possible reasons: (1) Govt uses per-parent vs PE\u2019s household threshold, (2) Govt may include behavioural responses, (3) relatively few families earn \u00a3100k\u2013\u00a3150k AND have young children.",
  },

  // ── WORK REQUIREMENTS ──
  {
    category: "Work Requirements",
    reform: "Remove 16hr/week work requirement entirely (reduce to 1hr minimum)",
    context: "Remove the 16hrs/week minimum work requirement for TFC and extended entitlement (reduce to 1hr). Opens eligibility to non-working and part-time families.",
    pe: { analysis: "min_work_hours", scenario: "No minimum (1 hr)", metric: "delta" },
    extValue: 250e6,
    extLabel: "Sutton Trust / IFS \u2014 A Fair Start (remove work req for 3\u20134yr-olds only)",
    sourceUrl: "https://www.suttontrust.com/our-research/a-fair-start-equalising-access-to-early-education/",
    sourceRef: "Section 5, Table 5.1: \u2018Universalising the entitlement\u2019 row, central scenario (\u00a3250m)",
    comparability: "similar",
    whyDiffer: "PE removes work requirement for ALL ECE ages (9m\u20134) plus TFC. Sutton Trust costs this only for 3\u20134yr-olds\u2019 extended entitlement. PE\u2019s broader scope (younger children cost more per funded hour, plus TFC) explains the gap.",
  },

  // ── TARGETED ELIGIBILITY ──
  {
    category: "Targeted Eligibility",
    reform: "Raise UC income threshold for targeted 2yr-old entitlement to \u00a330k (vs extending 30hrs to disadvantaged 2yr-olds)",
    context: "Raise the UC income threshold for 2yr-old targeted entitlement from \u00a315,400 to \u00a330k. Compared against Sutton Trust\u2019s different reform: extending 30hrs to disadvantaged 2yr-olds.",
    pe: { analysis: "targeted_eligibility", scenario: "UC limit \u00a330k", metric: "delta" },
    extValue: 165e6,
    extLabel: "Sutton Trust / IFS \u2014 30hrs for disadvantaged 3\u20134yr-olds",
    sourceUrl: "https://www.suttontrust.com/our-research/a-fair-start-equalising-access-to-early-education/",
    sourceRef: "Section 5, Table 5.1: \u2018Extending 30hrs to disadvantaged 3\u20134yr-olds\u2019 row, central scenario (\u00a3165m)",
    comparability: "different",
    whyDiffer: "Different reforms entirely. PE raises the UC income threshold to \u00a330k for the 15hr targeted entitlement (narrow). Sutton Trust costs giving 30hrs extended entitlement to disadvantaged 3\u20134yr-olds (much broader). Divergence is expected because these are fundamentally different policy levers.",
  },
];

const CATEGORY_ORDER = [
  "Extended Entitlement",
  "Provider Funding Rates",
  "Reform Bundles",
  "Baseline Spending",
  "UC Childcare Caps",
  "Funded Weeks per Year",
  "UC Childcare Coverage",
  "Income Cap",
  "Work Requirements",
  "Targeted Eligibility",
];

const COMPARABILITY_LABELS = {
  "like-for-like": "Like-for-like",
  "similar": "Similar scope",
  "different": "Different reforms",
  "pe-only": "PE only",
};

/* ── CSV lookup ──────────────────────────────────────────── */

function lookup(data, spec) {
  if (!spec) return null;
  const row = data.find(
    (r) => r.analysis === spec.analysis && r.scenario === spec.scenario && r.metric === spec.metric,
  );
  return row ? row.value : null;
}

/* ── App ─────────────────────────────────────────────────── */

export default function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/results.csv")
      .then((res) => (res.ok ? res.text() : Promise.reject()))
      .then((text) => {
        const { data: parsed } = Papa.parse(text, { header: true, skipEmptyLines: true });
        setData(parsed.map((r) => ({ ...r, value: parseFloat(r.value) })));
      })
      .catch(() => {});
  }, []);

  if (!data.length) {
    return (
      <div className="loading">
        <div className="loading-inner">
          <h1>UK Childcare Reforms Audit</h1>
          <p>Loading results\u2026</p>
          <p className="loading-hint">
            Run <code>python run.py all</code> and copy results to{" "}
            <code>dashboard/public/results.csv</code>
          </p>
        </div>
      </div>
    );
  }

  // Resolve values — PE from CSV, externals hardcoded
  const resolved = COMPARISONS.map((c) => {
    const peVal = lookup(data, c.pe);
    const extVal = c.extValue ?? null;
    const isPeOnly = c.comparability === "pe-only";
    const match = isPeOnly ? "none" : getMatch(peVal, extVal);
    const diff = pct(peVal, extVal);
    return { ...c, peVal, extVal, match, diff, isPeOnly };
  });

  // Group by category
  const grouped = CATEGORY_ORDER.map((cat) => ({
    category: cat,
    items: resolved.filter((c) => c.category === cat),
  })).filter((g) => g.items.length > 0);

  // Counts
  const counts = { close: 0, moderate: 0, divergent: 0, none: 0 };
  resolved.forEach((c) => counts[c.match]++);
  const total = resolved.length;

  return (
    <>
      <header className="header">
        <h1>UK Childcare Reforms Audit</h1>
        <p className="header-sub">PolicyEngine vs External Estimates</p>
      </header>

      <div className="intro">
        Comparing{" "}
        <a href="https://policyengine.org/uk" target="_blank" rel="noreferrer">PolicyEngine UK</a>{" "}
        microsimulation estimates against published costings from OBR, IFS, HMRC, DfE, HM Treasury,
        CPAG, Sutton Trust, Women&apos;s Budget Group, and Resolution Foundation. Each comparison
        shows what PolicyEngine estimates, what the external source says, and why they differ.{" "}
        <a href="https://policyengine.org/uk/research/uk-childcare-report" target="_blank" rel="noreferrer">
          Full methodology &rarr;
        </a>
      </div>

      <div className="summary-bar">
        <div className="summary-item">
          <span className="summary-num">{total}</span>
          <span className="summary-label">Comparisons</span>
        </div>
        <div className="summary-item">
          <span className="pill pill-close">{counts.close}</span>
          <span className="summary-label">Close (&le;20%)</span>
        </div>
        <div className="summary-item">
          <span className="pill pill-moderate">{counts.moderate}</span>
          <span className="summary-label">Moderate</span>
        </div>
        <div className="summary-item">
          <span className="pill pill-divergent">{counts.divergent}</span>
          <span className="summary-label">Large gap</span>
        </div>
      </div>

      <main className="main">
        {grouped.map((group) => (
          <section key={group.category} className="cat-section">
            <h2 className="cat-title">{group.category}</h2>

            {group.items.map((c, i) => (
              <div key={i} className={`comp-card border-${c.match}`}>
                {/* Card header */}
                <div className="comp-header">
                  <div className="comp-reform">{c.reform}</div>
                  <div className="comp-badges">
                    <span className={`comp-badge badge-${c.comparability === "pe-only" ? "none" : c.comparability}`}>
                      {COMPARABILITY_LABELS[c.comparability]}
                    </span>
                    <span className={`comp-badge badge-${c.match}`}>
                      {MATCH_LABELS[c.match]}
                    </span>
                  </div>
                </div>

                {/* Policy context */}
                {c.context && (
                  <div className="comp-context">{c.context}</div>
                )}

                {/* Estimates */}
                <div className="comp-estimates">
                  <div className="est est-pe">
                    <div className="est-who">PolicyEngine</div>
                    <div className="est-val">{fmt(c.peVal)}</div>
                  </div>

                  {!c.isPeOnly && (
                    <>
                      <div className="est-vs">vs</div>
                      <div className="est est-ext">
                        <div className="est-who">
                          {c.extLabel}
                          {c.extNote && <span className="est-note"> &mdash; {c.extNote}</span>}
                        </div>
                        <div className="est-val">{fmt(c.extVal)}</div>
                      </div>
                    </>
                  )}
                </div>

                {/* Difference indicator */}
                {!c.isPeOnly && c.diff != null && (
                  <div className={`comp-diff diff-${c.match}`}>
                    {c.diff > 0 ? "+" : ""}{c.diff}% difference
                    {c.peVal && c.extVal && (
                      <span className="diff-ratio">
                        {" "}({(c.peVal / c.extVal).toFixed(2)}x)
                      </span>
                    )}
                  </div>
                )}

                {/* Source */}
                {c.sourceUrl && (
                  <div className="comp-source">
                    <a href={c.sourceUrl} target="_blank" rel="noreferrer">
                      Source &rarr;
                    </a>
                    {c.sourceRef && <span className="source-ref"> &mdash; {c.sourceRef}</span>}
                  </div>
                )}

                {/* Why they differ */}
                {c.whyDiffer && (
                  <div className={`comp-why why-${c.match}`}>
                    <strong>
                      {c.isPeOnly ? "Context:" : c.match === "close" ? "Assessment:" : "Why they differ:"}
                    </strong>{" "}
                    {c.whyDiffer}
                  </div>
                )}
              </div>
            ))}
          </section>
        ))}
      </main>

      <footer className="app-footer">
        Built with{" "}
        <a href="https://policyengine.org/uk" target="_blank" rel="noreferrer">PolicyEngine UK</a>
        {" "}microsimulation &middot; Data from <code>output/results_2026.csv</code> &middot;{" "}
        <a href="https://policyengine.org/uk/research/uk-childcare-report" target="_blank" rel="noreferrer">
          Full report
        </a>
      </footer>
    </>
  );
}
