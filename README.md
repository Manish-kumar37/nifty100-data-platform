# Sprint 1 - Day 1
## Environment Setup

### Objective
Set up the development environment and project structure for the NIFTY 100 Data Platform.

---

## Tasks Completed

### Project Structure

Created the initial project directories:

```text
nifty100-project/
│
├── data/
│   └── raw/
│
├── src/
│   └── etl/
│
├── db/
│
├── tests/
│   └── etl/
│
├── output/
│
├── notebooks/
│
└── docs/
```

---

### Virtual Environment

Created and activated a Python virtual environment.

```bash
python -m venv venv
```

Activation:

```bash
venv\Scripts\activate
```

---

### Dependencies Installed

Core libraries installed:

```bash
pip install pandas
pip install openpyxl
pip install numpy
pip install pytest
pip install sqlalchemy
```

Additional utilities:

- pathlib
- sqlite3
- os
- logging

---

### Configuration

Created:

```text
.env
.gitignore
requirements.txt
```

---

### Git Setup

Initialized local Git repository.

```bash
git init
```

Configured:

```bash
git config --global user.name "<your-name>"
git config --global user.email "<your-email>"
```

---

### Database Planning

Defined initial database architecture:

- Companies
- Profit & Loss
- Balance Sheet
- Cash Flow
- Analysis
- Documents
- Pros & Cons
- Sectors
- Peer Groups
- Financial Ratios
- Stock Prices

---

## Deliverables

- Project structure created
- Virtual environment configured
- Required libraries installed
- Git initialized
- Configuration files created
- Database design finalized

---

## Outcome

Environment successfully prepared for ETL development and database implementation.

Sprint Status:

✅ Day 1 Completed

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

## Project Status

| Sprint | Status |
|---------|--------|
| Sprint 1 – Data Foundation | ✅ Completed |
| Sprint 2 – Financial Analytics Engine | ✅ Completed |
| Sprint 3 – Financial Screener & Peer Analytics | ✅ Completed |
| Sprint 4 – Upcoming | ⏳ |

## Features

### Data Pipeline
- ETL pipeline for NIFTY 100 financial data
- SQLite database
- Data validation and quality checks

### Financial Analytics
- 10+ financial ratio calculations
- Revenue, PAT, and EPS CAGR
- Composite Quality Score
- Sector-relative scoring

### Stock Screener
- Custom threshold-based screening
- 6 preset screeners
- YAML-configurable filters
- Excel export

### Peer Analytics
- Peer percentile rankings
- Benchmark company identification
- Radar chart generation
- Peer comparison Excel report

src/
│
├── analytics/
│   ├── engine.py
│   ├── peer.py
│   ├── peer_report.py
│   ├── radar.py
│   └── scoring.py
│
├── screener/
│   ├── engine.py
│   └── export.py
│
├── etl/
├── database/
└── tests/

config/
output/
reports/
db/

## Generated Reports

### Excel Reports

- screener_output.xlsx
- peer_comparison.xlsx

### Visual Reports

- Radar charts for all peer-group companies

### Database

- financial_ratios
- peer_percentiles

## Tech Stack

- Python
- Pandas
- SQLite
- OpenPyXL
- Matplotlib
- YAML
- Git

## Current Project Statistics

- 92 Companies
- 1,164 Financial Ratio Records
- 56 Peer Group Companies
- 11 Peer Groups
- 560 Percentile Rankings
- 56 Radar Charts

## Sprint Progress

Sprint 1  ██████████ 100%

Sprint 2  ██████████ 100%

Sprint 3  ██████████ 100%

Sprint 4  ░░░░░░░░░░   0%

## Upcoming

- Sprint 4 – Portfolio & Watchlist
- Sprint 5 – Forecasting
- Dashboard Deployment
- REST API

## Backlog / Future Improvements

- Improve ROE calculation methodology
- Add P/E, P/B, Dividend Yield and Market Cap support
- Add conditional formatting to Excel reports
- Refactor shared helper functions
- Optimize report generation performance