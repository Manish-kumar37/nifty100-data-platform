# Sprint 2 – Financial Ratio Engine

## Sprint Duration

Day 08 – Day 14

## Sprint Goal

Develop a Financial Ratio Engine capable of computing key financial KPIs for all companies across available financial years and storing the results in the SQLite database.

---

## Features Implemented

### Profitability Ratios
- Net Profit Margin
- Operating Profit Margin
- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Return on Assets (ROA)

### Leverage Ratios
- Debt-to-Equity Ratio
- Interest Coverage Ratio
- Asset Turnover Ratio

### Cash Flow KPIs
- Free Cash Flow
- Capital Allocation Classification

### CAGR Engine
- Revenue CAGR (3Y, 5Y, 10Y)
- PAT CAGR (3Y, 5Y, 10Y)
- EPS CAGR (3Y, 5Y, 10Y)

### Edge Cases Handled
- Zero denominator
- Negative equity
- Debt-free companies
- Zero base CAGR
- Turnaround
- Decline to loss
- Both negative
- Insufficient history

---

## Database Output

Table:

```
financial_ratios
```

Rows Generated:

```
1164
```

KPI columns added:

- net_profit_margin_pct
- operating_profit_margin_pct
- return_on_equity_pct
- return_on_capital_employed_pct
- return_on_assets_pct
- debt_to_equity
- interest_coverage
- asset_turnover
- free_cash_flow_cr
- capital_allocation
- revenue_cagr_3yr
- revenue_cagr_5yr
- revenue_cagr_10yr
- pat_cagr_3yr
- pat_cagr_5yr
- pat_cagr_10yr
- eps_cagr_3yr
- eps_cagr_5yr
- eps_cagr_10yr

---

## Reports Generated

- output/capital_allocation.csv
- output/ratio_edge_cases.log

---

## Testing

```
pytest tests/kpi -v
```

Result:

```
36 tests passed
```

---

## Validation

- financial_ratios table populated successfully
- 1164 company-year records generated
- Foreign key validation passed
- KPI calculations verified

---

## Sprint Outcome

Sprint 2 completed successfully with a fully functional Financial Ratio Engine capable of calculating and storing financial KPIs for all available company-year records.