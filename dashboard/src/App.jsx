import { useState, useEffect, useCallback } from "react";
import Papa from "papaparse";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  CartesianGrid,
  Legend,
} from "recharts";

const COLORS = [
  "#2d6a4f",
  "#40916c",
  "#52b788",
  "#74c69d",
  "#95d5b2",
  "#1b4332",
  "#376e54",
  "#5e9c7e",
];

const ANALYSIS_LABELS = {
  baseline: "Baseline spending",
  takeup: "Take-up sensitivity",
  uc_coverage: "UC coverage rate",
  uc_caps: "UC caps",
  extended_hours: "Extended hours",
  tfc_rate: "TFC rate",
  tfc_caps: "TFC caps",
  income_cap: "Income cap",
  funding_rates: "Funding rates",
  targeted_eligibility: "Targeted eligibility",
  extend_weeks: "Weeks per year",
  min_work_hours: "Minimum work hours",
  fiscal: "Net fiscal impact",
};

const METRIC_LABELS = {
  tax_free_childcare: "Tax-Free Childcare",
  uc_childcare_element: "UC childcare element",
  WTC_childcare_element: "WTC childcare element",
  universal_childcare_entitlement: "Universal entitlement",
  targeted_childcare_entitlement: "Targeted entitlement",
  extended_childcare_entitlement: "Extended entitlement",
  care_to_learn: "Care to Learn",
  total: "Total",
  delta: "Change vs baseline",
  net_cost: "Net cost",
  total_gain: "Total gain",
  avg_gain_per_hh: "Average gain per household",
  Combined: "Combined",
  UCE: "Universal",
  TCE: "Targeted",
  ECE: "Extended",
  TFC: "Tax-Free Childcare",
  "UC CC": "UC childcare",
};

const BENCHMARKS = {
  baseline: {
    description: "This section shows PolicyEngine UK\u2019s estimate of total annual government spending on each of the seven childcare programmes under current law. It serves as the reference point for all reform scenarios below.",
    baseline: "Current policy as legislated for the selected year, with PolicyEngine-calibrated take-up rates applied.",
    comparisons: [
      "PolicyEngine report (2025): TFC \u00a30.7bn, extended \u00a34.4bn, universal \u00a31.8bn, targeted \u00a30.5bn",
      "Government reported (2024): TFC \u00a30.6bn, extended \u00a32.5bn, universal \u00a31.7bn, targeted \u00a30.6bn, UC childcare ~\u00a31.0bn",
      "IFS: total early years spending ~\u00a38.7bn in 2025\u201326",
      "OBR: 2023 childcare expansion alone ~\u00a33.3bn in 2025\u201326",
    ],
    sources: [
      { label: "PolicyEngine childcare report (June 2025)", url: "https://www.policyengine.org/uk/research/uk-childcare-report" },
      { label: "HMRC TFC statistics (September 2025)", url: "https://www.gov.uk/government/statistics/tax-free-childcare-statistics-september-2025" },
      { label: "IFS education spending 2025\u201326", url: "https://ifs.org.uk/publications/annual-report-education-spending-england-2025-26" },
      { label: "OBR Spring Budget 2023 costings", url: "https://obr.uk/docs/dlm_uploads/Annexes-March-2023.pdf" },
    ],
  },
  takeup: {
    description: "This section tests how sensitive each programme\u2019s spending is to different take-up assumptions. PolicyEngine calibrates take-up rates to match official caseload data; here we vary them from 25% to 100% to show the range of possible costs.",
    baseline: "PolicyEngine-calibrated take-up rates: TFC 58%, extended 81%, universal 56%, targeted 60% (from PolicyEngine report Table 9, matched to government caseloads).",
    comparisons: [
      "Government caseloads (2024): TFC 660k, extended 740k, universal 490k, targeted 130k children",
      "Approximately 63% of children aged 0\u20134 use formal childcare (DfE 2023 survey)",
      "IFS: only around 40% of eligible families are aware of Tax-Free Childcare",
      "Coram 2024: parental awareness of entitlements remains low",
    ],
    sources: [
      { label: "PolicyEngine childcare report (Tables 8\u20139)", url: "https://www.policyengine.org/uk/research/uk-childcare-report" },
      { label: "DfE childcare and early years survey 2023", url: "https://www.gov.uk/government/statistics/childcare-and-early-years-survey-of-parents-2023" },
      { label: "Coram childcare survey 2024", url: "https://www.coram.org.uk/resource/childcare-survey-2024" },
    ],
  },
  uc_coverage: {
    description: "Universal Credit covers 85% of eligible childcare costs. This analysis models what happens if the coverage rate is raised to 90%, 95%, or 100%, showing the additional fiscal cost of closing the 15% parental co-pay gap.",
    baseline: "Current UC childcare coverage rate: 85% (set by the Universal Credit (Childcare Costs) Regulations 2023). DWP reports approximately \u00a31.0bn total spend on the childcare element in 2023\u201324.",
    comparisons: [
      "Resolution Foundation recommends increasing to 100% coverage to remove the upfront cost barrier",
      "IPPR childcare guarantee also proposes 100% coverage",
      "DWP Stat-Xplore: UC childcare element spend approximately \u00a31.0bn in 2023\u201324",
    ],
    sources: [
      { label: "Resolution Foundation \u2013 Costly childcare (2023)", url: "https://www.resolutionfoundation.org/publications/costly-childcare/" },
      { label: "IPPR \u2013 A childcare guarantee (2024)", url: "https://www.ippr.org/articles/a-childcare-guarantee" },
      { label: "UC childcare costs regulations 2023", url: "https://www.legislation.gov.uk/uksi/2023/752/contents/made" },
    ],
  },
  uc_caps: {
    description: "UC childcare support is subject to monthly caps. This analysis models the effect of raising these caps by 50% and doubling them, to assess how many families are currently constrained by the ceiling.",
    baseline: "Current caps: \u00a31,014.63 per month for one child, \u00a31,739.37 per month for two or more children (2024\u201325 rates). Last uprated in 2023 alongside the coverage increase to 85%.",
    comparisons: [
      "Resolution Foundation: caps have not kept pace with rising childcare costs",
      "Average childcare cost for under-twos: approximately \u00a3300 per week in London, \u00a3250 per week nationally (Coram 2024)",
    ],
    sources: [
      { label: "Resolution Foundation \u2013 Costly childcare", url: "https://www.resolutionfoundation.org/publications/costly-childcare/" },
      { label: "DWP benefit and pension rates 2024\u201325", url: "https://www.gov.uk/government/publications/benefit-and-pension-rates-2024-to-2025" },
    ],
  },
  extended_hours: {
    description: "The extended childcare entitlement provides 30 funded hours per week to working families with children aged 1\u20134. This analysis models full rollout of 30 hours to all ages 1\u20134 and an IPPR-style 40 hours per week wrap-around scenario.",
    baseline: "Current policy: 30 hours per week, phased rollout. From September 2025, all eligible working families with children aged 9 months to 4 years can access 30 funded hours.",
    comparisons: [
      "OBR: 2023 expansion costs \u00a33.3bn in 2025\u201326, rising to \u00a34.1bn by 2027\u201328",
      "IPPR proposes 40 hours per week wrap-around for ages 0\u201311: \u00a317.8bn gross cost",
      "IFS: spending could end up \u00a31bn higher than initial forecasts owing to high take-up",
    ],
    sources: [
      { label: "OBR Spring Budget 2023 costings", url: "https://obr.uk/docs/dlm_uploads/Annexes-March-2023.pdf" },
      { label: "IPPR \u2013 A childcare guarantee", url: "https://www.ippr.org/articles/a-childcare-guarantee" },
      { label: "Childcare Act 2016", url: "https://www.legislation.gov.uk/ukpga/2016/5/contents" },
    ],
  },
  tfc_rate: {
    description: "Tax-Free Childcare gives parents a 20% government top-up on childcare spending. This analysis models what happens if the top-up rate is increased to 25%, 33%, or 50%.",
    baseline: "Current TFC rate: 20% (\u00a32 for every \u00a38 parents pay, up to \u00a32,000 per child per year). HMRC reports TFC cost \u00a30.5bn in 2024\u201325 with 1.1 million families using it.",
    comparisons: [
      "HMRC: TFC government top-ups totalled \u00a3632m in 2024\u201325 (826,000 families)",
      "IFS: only around 40% of eligible families are aware of TFC; actual take-up is lower still",
    ],
    sources: [
      { label: "HMRC TFC statistics (September 2025)", url: "https://www.gov.uk/government/statistics/tax-free-childcare-statistics-september-2025" },
      { label: "IFS \u2013 The health of the early years sector", url: "https://ifs.org.uk/publications/health-early-years-sector" },
    ],
  },
  tfc_caps: {
    description: "Tax-Free Childcare is subject to annual caps on government top-ups. This analysis models raising the caps from \u00a32,000/\u00a34,000 to \u00a33,000/\u00a36,000 and \u00a34,000/\u00a38,000 to assess how many families are constrained by the current ceiling.",
    baseline: "Current caps: \u00a32,000 per child per year (standard), \u00a34,000 per disabled child per year. HMRC reports an average quarterly TFC payment of approximately \u00a3400.",
    comparisons: [
      "HMRC: average quarterly payment of approximately \u00a3400 suggests most families do not hit the cap",
      "Higher-cost areas (e.g. London) are more likely to be cap-constrained",
    ],
    sources: [
      { label: "HMRC TFC statistics (September 2025)", url: "https://www.gov.uk/government/statistics/tax-free-childcare-statistics-september-2025" },
      { label: "Childcare Payments Act 2014", url: "https://www.legislation.gov.uk/ukpga/2014/28/contents" },
    ],
  },
  income_cap: {
    description: "Tax-Free Childcare and the extended entitlement are limited to families where each parent earns below \u00a3100,000 adjusted net income. This analysis models raising that cap to \u00a3150,000, \u00a3200,000, or removing it entirely.",
    baseline: "Current cap: \u00a3100,000 adjusted net income per parent. Applies to both TFC and the extended childcare entitlement (30 hours).",
    comparisons: [
      "IFS: higher earners benefit disproportionately from TFC compared with UC families",
      "Removing the cap would extend eligibility to the highest-income families",
    ],
    sources: [
      { label: "IFS \u2013 The health of the early years sector", url: "https://ifs.org.uk/publications/health-early-years-sector" },
      { label: "HMRC TFC eligibility", url: "https://www.gov.uk/tax-free-childcare" },
    ],
  },
  funding_rates: {
    description: "DfE funds childcare providers at hourly rates that vary by child age. This analysis models the cost of increasing these rates by 20%, 50%, or doubling them, addressing concerns about provider underfunding.",
    baseline: "Current DfE national average funding rates (2024\u201325): under-twos \u00a311.22 per hour, age 2 \u00a38.28 per hour, age 3+ \u00a35.88 per hour.",
    comparisons: [
      "Women\u2019s Budget Group: total funding needed \u00a39.4bn versus current \u00a34.2bn (gap of \u00a35.2bn in 2025\u201326)",
      "Ceeda/DfE provider cost study 2024 highlights systemic underfunding across the sector",
      "IFS: funding rates largely protected in real terms, but the disadvantage premium received a significant uplift",
    ],
    sources: [
      { label: "Women\u2019s Budget Group \u2013 Childcare funding gap", url: "https://wbg.org.uk/analysis/the-childcare-funding-gap/" },
      { label: "DfE early years funding rates 2024\u201325", url: "https://www.gov.uk/government/publications/early-years-funding-2024-to-2025" },
      { label: "IFS education spending 2025\u201326", url: "https://ifs.org.uk/publications/annual-report-education-spending-england-2025-26" },
    ],
  },
  targeted_eligibility: {
    description: "The targeted (disadvantaged two-year-old) entitlement is means-tested via UC and tax credit income thresholds. This analysis models what happens if the UC income limit is raised from \u00a315,400 to \u00a320,000, \u00a325,000, or \u00a330,000.",
    baseline: "Current income limits: UC income below \u00a315,400; tax credit income below \u00a316,190. DfE reports approximately 72% of eligible two-year-olds take up funded places.",
    comparisons: [
      "DfE: approximately 72% take-up among eligible two-year-olds",
      "Raising the threshold would extend eligibility to more low-to-middle income families",
    ],
    sources: [
      { label: "DfE \u2013 Education provision: children under 5", url: "https://explore-education-statistics.service.gov.uk/find-statistics/education-provision-children-under-5" },
      { label: "DfE \u2013 Free early education for two-year-olds", url: "https://www.gov.uk/help-with-childcare-costs/free-childcare-2-year-olds" },
    ],
  },
  extend_weeks: {
    description: "Funded childcare entitlements currently run for 38 weeks per year (term-time only). This analysis models extending provision to 44, 48 (IPPR proposal), and 52 weeks (full year) to address the holiday childcare gap.",
    baseline: "Current: 38 weeks per year (term-time only). Parents must self-fund the remaining 14 weeks of holiday childcare.",
    comparisons: [
      "Resolution Foundation: 25 hours per week for 47 weeks for three- and four-year-olds costs approximately \u00a32.1bn",
      "IPPR proposes 48 weeks per year as part of their universal guarantee",
      "Holiday childcare costs average \u00a3150 per week per child (Coram 2024)",
    ],
    sources: [
      { label: "Resolution Foundation \u2013 An equal start", url: "https://www.resolutionfoundation.org/publications/an-equal-start/" },
      { label: "IPPR \u2013 A childcare guarantee", url: "https://www.ippr.org/articles/a-childcare-guarantee" },
    ],
  },
  min_work_hours: {
    description: "Tax-Free Childcare and the extended entitlement require each parent to work at least 16 hours per week. This analysis models lowering that threshold to 12, 8, or 1 hour to extend eligibility to part-time workers.",
    baseline: "Current: 16 hours per week minimum (equivalent to 16 hours at the national minimum or living wage). Applies to both TFC and the extended childcare entitlement.",
    comparisons: [
      "Resolution Foundation: a part-time cleaner working 10 hours per week loses \u00a37 per week compared with not working at all, owing to lost childcare support",
      "TUC: childcare costs are a major barrier to part-time workers entering or remaining in employment",
    ],
    sources: [
      { label: "Resolution Foundation \u2013 Costly childcare", url: "https://www.resolutionfoundation.org/publications/costly-childcare/" },
      { label: "TUC \u2013 Childcare and working families", url: "https://www.tuc.org.uk/research-analysis/reports/childcare-and-working-families" },
    ],
  },
  fiscal: {
    description: "This section estimates the net fiscal cost of four composite reform bundles by comparing reformed household net income against the baseline. Each bundle combines multiple parameter changes into a single coherent reform package.",
    baseline: "Net cost equals the total increase in household net income under each reform minus the baseline. A positive value means the reform costs the government more.",
    comparisons: [
      "IFS: 2023 expansion revised cost approximately \u00a31bn higher than initially forecast",
      "IPPR universal guarantee: \u00a37.7bn net fiscal cost (offset by \u00a38bn in parental employment gains)",
      "Himmelweit and Sevilla (Women\u2019s Budget Group): \u00a37.3\u201317.9bn net depending on the scope of universal childcare",
      "Resolution Foundation: 25 hours per week for 47 weeks for three- and four-year-olds costs approximately \u00a32.1bn net",
    ],
    sources: [
      { label: "IFS education spending 2025\u201326", url: "https://ifs.org.uk/publications/annual-report-education-spending-england-2025-26" },
      { label: "IPPR \u2013 A childcare guarantee", url: "https://www.ippr.org/articles/a-childcare-guarantee" },
      { label: "Women\u2019s Budget Group \u2013 Childcare as infrastructure", url: "https://wbg.org.uk/analysis/a-new-approach-to-childcare/" },
      { label: "Resolution Foundation \u2013 An equal start", url: "https://www.resolutionfoundation.org/publications/an-equal-start/" },
    ],
  },
};

function fmtBn(v) {
  const abs = Math.abs(v);
  if (abs >= 1e9) return `\u00A3${(v / 1e9).toFixed(2)}bn`;
  if (abs >= 1e6) return `\u00A3${(v / 1e6).toFixed(0)}m`;
  return `\u00A3${v.toLocaleString("en-GB", { maximumFractionDigits: 0 })}`;
}

function labelOf(key, map) {
  return map[key] || key;
}

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 8,
        padding: "0.5rem 0.75rem",
        fontSize: "0.8rem",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ color: "#000", fontWeight: 600 }}>{d.name}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color || "#000" }}>
          {p.name}: {fmtBn(p.value)}
        </div>
      ))}
    </div>
  );
}

function BenchmarkBox({ analysisKey }) {
  const b = BENCHMARKS[analysisKey];
  if (!b) return null;
  return (
    <div className="benchmark-box">
      <p style={{ marginBottom: "0.5rem" }}>{b.description}</p>
      <strong>Reform baseline:</strong> {b.baseline}
      <div style={{ marginTop: "0.5rem" }}>
        <strong>Comparable estimates:</strong>
        <ul>
          {b.comparisons.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      </div>
      <div style={{ marginTop: "0.5rem", fontSize: "0.78rem" }}>
        Sources:{" "}
        {b.sources.map((s, i) => (
          <span key={i}>
            {i > 0 && " | "}
            <a href={s.url} target="_blank" rel="noreferrer">
              {s.label}
            </a>
          </span>
        ))}
      </div>
    </div>
  );
}

// ── Sections ────────────────────────────────────────────────────

function BaselineSection({ rows }) {
  const items = rows
    .filter((r) => r.metric !== "total")
    .map((r) => ({
      name: labelOf(r.metric, METRIC_LABELS),
      value: r.value,
    }))
    .sort((a, b) => b.value - a.value);

  const total = rows.find((r) => r.metric === "total");

  return (
    <div className="card">
      <h2>Baseline childcare spending</h2>
      <BenchmarkBox analysisKey="baseline" />
      {total && (
        <div className="summary-grid">
          <div className="stat-card">
            <div className="label">Total annual spending</div>
            <div className="value">{fmtBn(total.value)}</div>
          </div>
          <div className="stat-card">
            <div className="label">Year</div>
            <div className="value">{total.year}</div>
          </div>
          <div className="stat-card">
            <div className="label">Programmes</div>
            <div className="value">{items.length}</div>
          </div>
        </div>
      )}
      <div className="chart-container">
        <ResponsiveContainer>
          <BarChart data={items} layout="vertical" margin={{ left: 160 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              type="number"
              tickFormatter={fmtBn}
              stroke="#000"
              fontSize={12}
              tick={{ fill: "#000" }}
            />
            <YAxis
              type="category"
              dataKey="name"
              stroke="#000"
              fontSize={12}
              width={150}
              tick={{ fill: "#000" }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {items.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function ScenarioSection({ analysisKey, rows }) {
  const nonDelta = rows.filter((r) => r.metric !== "delta");

  const metrics = [...new Set(nonDelta.map((r) => r.metric))];
  const scenarios = [...new Set(nonDelta.map((r) => r.scenario))];

  const chartData = scenarios.map((sc) => {
    const entry = { name: sc };
    metrics.forEach((m) => {
      const found = nonDelta.find(
        (r) => r.scenario === sc && r.metric === m
      );
      if (found) entry[m] = found.value;
    });
    return entry;
  });

  return (
    <div className="card">
      <h2>{labelOf(analysisKey, ANALYSIS_LABELS)}</h2>
      <BenchmarkBox analysisKey={analysisKey} />
      <div className="chart-container tall">
        <ResponsiveContainer>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="name"
              stroke="#000"
              fontSize={11}
              tick={{ fill: "#000" }}
              interval={0}
            />
            <YAxis
              tickFormatter={fmtBn}
              stroke="#000"
              fontSize={12}
              tick={{ fill: "#000" }}
            />
            <Tooltip content={<CustomTooltip />} />
            {metrics.length > 1 && <Legend />}
            {metrics.map((m, i) => (
              <Bar
                key={m}
                dataKey={m}
                name={labelOf(m, METRIC_LABELS)}
                fill={COLORS[i % COLORS.length]}
                radius={[4, 4, 0, 0]}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function TakeupSection({ rows }) {
  const schemes = [...new Set(rows.map((r) => r.scenario))];

  return (
    <div className="card">
      <h2>Take-up sensitivity</h2>
      <BenchmarkBox analysisKey="takeup" />
      {schemes.map((scheme) => {
        const schemeRows = rows.filter((r) => r.scenario === scheme);
        const calibrated = schemeRows.find((r) =>
          r.metric.startsWith("calibrated_")
        );
        const sensitivity = schemeRows
          .filter((r) => r.metric.startsWith("takeup_"))
          .map((r) => ({
            name: `${(parseFloat(r.metric.split("_")[1]) * 100).toFixed(0)}%`,
            value: r.value,
          }));

        return (
          <div key={scheme}>
            <h3>
              {scheme}
              {calibrated && (
                <span
                  style={{
                    fontSize: "0.8rem",
                    color: "#000",
                    fontWeight: 400,
                    marginLeft: "0.75rem",
                  }}
                >
                  Calibrated: {fmtBn(calibrated.value)}
                </span>
              )}
            </h3>
            <div className="chart-container" style={{ height: 200 }}>
              <ResponsiveContainer>
                <BarChart data={sensitivity}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" stroke="#000" fontSize={12} tick={{ fill: "#000" }} />
                  <YAxis
                    tickFormatter={fmtBn}
                    stroke="#000"
                    fontSize={12}
                    tick={{ fill: "#000" }}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar
                    dataKey="value"
                    fill="#2d6a4f"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function FiscalSection({ rows }) {
  const data = rows.map((r) => ({
    name: r.scenario,
    value: r.value,
  }));

  return (
    <div className="card">
      <h2>Net fiscal impact</h2>
      <BenchmarkBox analysisKey="fiscal" />
      <div className="summary-grid">
        {data.map((d, i) => (
          <div className="stat-card" key={i}>
            <div className="label">{d.name}</div>
            <div className={`value ${d.value >= 0 ? "positive" : "negative"}`}>
              {fmtBn(d.value)}
            </div>
          </div>
        ))}
      </div>
      <div className="chart-container">
        <ResponsiveContainer>
          <BarChart data={data} layout="vertical" margin={{ left: 220 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              type="number"
              tickFormatter={fmtBn}
              stroke="#000"
              fontSize={12}
              tick={{ fill: "#000" }}
            />
            <YAxis
              type="category"
              dataKey="name"
              stroke="#000"
              fontSize={11}
              width={210}
              tick={{ fill: "#000" }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {data.map((d, i) => (
                <Cell
                  key={i}
                  fill={d.value >= 0 ? "#16a34a" : "#dc2626"}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function DistributionalSection({ rows }) {
  const gains = rows
    .filter(
      (r) => r.metric === "total_gain" && r.scenario !== "all"
    )
    .map((r) => {
      const decile = r.scenario.replace("decile_", "");
      const avg = rows.find(
        (x) =>
          x.scenario === r.scenario && x.metric === "avg_gain_per_hh"
      );
      return {
        name: `D${decile}`,
        total_gain: r.value,
        avg_gain: avg ? avg.value : 0,
      };
    });

  const totalRow = rows.find(
    (r) => r.scenario === "all" && r.metric === "total_gain"
  );

  return (
    <div className="card">
      <h2>Distributional analysis</h2>
      {totalRow && (
        <div className="summary-grid">
          <div className="stat-card">
            <div className="label">Total gain (all deciles)</div>
            <div className="value positive">{fmtBn(totalRow.value)}</div>
          </div>
        </div>
      )}
      <h3>Total gain by income decile</h3>
      <div className="chart-container">
        <ResponsiveContainer>
          <BarChart data={gains}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="name" stroke="#000" fontSize={12} tick={{ fill: "#000" }} />
            <YAxis
              tickFormatter={fmtBn}
              stroke="#000"
              fontSize={12}
              tick={{ fill: "#000" }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar
              dataKey="total_gain"
              name="Total gain"
              radius={[4, 4, 0, 0]}
            >
              {gains.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <h3>Average gain per household</h3>
      <div className="chart-container">
        <ResponsiveContainer>
          <BarChart data={gains}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="name" stroke="#000" fontSize={12} tick={{ fill: "#000" }} />
            <YAxis
              tickFormatter={(v) =>
                `\u00A3${v.toLocaleString("en-GB", {
                  maximumFractionDigits: 0,
                })}`
              }
              stroke="#000"
              fontSize={12}
              tick={{ fill: "#000" }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar
              dataKey="avg_gain"
              name="Average gain per household"
              fill="#40916c"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

// ── Main app ────────────────────────────────────────────────────

export default function App() {
  const [data, setData] = useState([]);
  const [tab, setTab] = useState("overview");

  const loadCSV = useCallback((text) => {
    const { data: parsed } = Papa.parse(text, {
      header: true,
      skipEmptyLines: true,
    });
    const rows = parsed.map((r) => ({
      ...r,
      value: parseFloat(r.value),
      year: parseInt(r.year, 10),
    }));
    setData(rows);
  }, []);

  useEffect(() => {
    fetch("/results.csv")
      .then((res) => {
        if (res.ok) return res.text();
        throw new Error("No CSV found");
      })
      .then(loadCSV)
      .catch(() => {});
  }, [loadCSV]);

  const analyses = [...new Set(data.map((r) => r.analysis))];
  const byAnalysis = (key) => data.filter((r) => r.analysis === key);

  const TABS = [
    { key: "overview", label: "Overview" },
    ...analyses
      .filter((a) => a !== "baseline" && a !== "distributional" && a !== "fiscal")
      .map((a) => ({
        key: a,
        label: ANALYSIS_LABELS[a] || a,
      })),
  ];

  if (data.length === 0) {
    return (
      <>
        <div className="banner">
          <h1>UK childcare reforms benchmark</h1>
        </div>
        <p className="intro">Loading results\u2026</p>
      </>
    );
  }

  const year = data[0]?.year;

  function renderTab() {
    if (tab === "overview") {
      return (
        <>
          {analyses.includes("baseline") && (
            <BaselineSection rows={byAnalysis("baseline")} />
          )}
          {analyses.includes("fiscal") && (
            <FiscalSection rows={byAnalysis("fiscal")} />
          )}
          {analyses.includes("distributional") && (
            <DistributionalSection rows={byAnalysis("distributional")} />
          )}
        </>
      );
    }

    const rows = byAnalysis(tab);
    if (rows.length === 0) {
      return <div className="empty">No data for this analysis.</div>;
    }

    if (tab === "takeup") return <TakeupSection rows={rows} />;
    if (tab === "fiscal") return <FiscalSection rows={rows} />;
    return <ScenarioSection analysisKey={tab} rows={rows} />;
  }

  return (
    <>
      <div className="banner">
        <h1>UK childcare reforms benchmark</h1>
      </div>

      <p className="intro">
        This tool uses the{" "}
        <a href="https://www.policyengine.org/uk" target="_blank" rel="noreferrer">
          PolicyEngine UK
        </a>{" "}
        microsimulation model to stress-test childcare subsidy reforms for the {year} tax year.
        Each section models a specific policy lever, compares the results against official government
        estimates and external benchmarks from the IFS, IPPR, Resolution Foundation, and the
        Women&apos;s Budget Group, and reports the fiscal cost of each reform. See the{" "}
        <a href="https://www.policyengine.org/uk/research/uk-childcare-report" target="_blank" rel="noreferrer">
          full report
        </a>{" "}
        for methodology.
      </p>

      <div className="tabs">
        {TABS.map((t) => (
          <button
            key={t.key}
            className={tab === t.key ? "active" : ""}
            onClick={() => setTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="content">
        {renderTab()}
      </div>
    </>
  );
}
