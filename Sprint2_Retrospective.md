# Sprint 2 Retrospective

## Sprint Goal

Developed a Financial Ratio Engine capable of computing profitability,
leverage, efficiency, cash flow, and CAGR metrics for all companies
across available financial years.

---

## Completed Work

- Implemented profitability ratios
  - Net Profit Margin
  - Operating Profit Margin
  - ROE
  - ROCE
  - ROA

- Implemented leverage ratios
  - Debt-to-Equity
  - Interest Coverage
  - Asset Turnover

- Implemented cash flow KPIs
  - Free Cash Flow
  - CFO Quality
  - CapEx Intensity
  - FCF Conversion
  - Capital Allocation Patterns

- Implemented CAGR engine
  - Revenue CAGR
  - PAT CAGR
  - EPS CAGR
  - 3-year
  - 5-year
  - 10-year

- Added edge-case handling
  - Zero denominator
  - Negative equity
  - Debt-free companies
  - Turnaround detection
  - Decline-to-loss
  - Zero base
  - Insufficient history

- Populated financial_ratios table.

---

## Challenges

- Duplicate financial records.
- Foreign key mismatches.
- CAGR edge-case debugging.
- Merge conflicts while building the ratio engine.

---

## Lessons Learned

- Financial ratios require careful denominator validation.
- CAGR calculations need dedicated edge-case handling.
- Banking companies require different leverage interpretation.
- Logging anomalies makes debugging significantly easier.

---

## Sprint Outcome

- Ratio Engine completed.
- 1164 company-year records processed.
- KPI unit tests passed successfully.
- Output reports generated successfully.