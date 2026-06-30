# NIFTY 100 DATA PLATFORM
## Sprint 1 Completion Report
### Sprint 1: Data Foundation (Day 01 – Day 07)

---

## Sprint Goal

Build a fully validated SQLite database (`nifty100.db`) from NIFTY 100 source files with ETL pipelines, data quality checks, audit logging, and automated testing.

---

# Deliverables Completed

## Database

Database Name:

`nifty100.db`

Tables Loaded:

- companies
- profitandloss
- balancesheet
- cashflow
- analysis
- documents
- prosandcons
- sectors
- peer_groups
- financial_ratios
- stock_prices

---

## Final Row Counts

| Table | Rows Loaded |
|---------|------------:|
| companies | 92 |
| profitandloss | 1164 |
| balancesheet | 1140 |
| cashflow | 1068 |
| analysis | 16 |
| documents | 1457 |
| prosandcons | 14 |
| sectors | 92 |
| peer_groups | 56 |
| financial_ratios | 1160 |
| stock_prices | 5520 |

---

## Foreign Key Validation

Validation Result:

```text
FK CHECK
[]
```

Result:

```text
PASS
```

No foreign key violations exist in the final database.

---

# Data Quality Validation

## DQ-01 Primary Key Uniqueness

Result:

```text
PASS
```

Companies PK duplicates:

```text
0
```

---

## DQ-02 Company-Year Uniqueness

Result:

```text
PASS
```

Duplicates removed:

```text
13
```

---

## DQ-03 Foreign Key Integrity

Result:

```text
PASS
```

Invalid company references removed before loading.

Affected records:

```text
99
```

---

## DQ-04 Balance Sheet Validation

Rule:

```text
Total Assets ≈ Total Liabilities
```

Result:

```text
4 warnings
```

No critical failures.

---

## DQ-05 OPM Cross Check

Result:

```text
234 warnings
```

Primarily due to financial-sector companies where OPM calculations differ from manufacturing businesses.

---

## DQ-06 Positive Sales Validation

Result:

```text
1 warning
```

---

## DQ-07 Tax Rate Validation

Rule:

```text
-100% <= Tax Rate <= 100%
```

Result:

```text
PASS
```

Failures:

```text
0
```

---

## DQ-08 EPS Sign Consistency

Result:

```text
1 warning
```

Affected Company:

```text
TATAPOWER
```

---

## DQ-09 Dividend Payout Validation

Rule:

```text
Dividend Payout <= 500%
```

Result:

```text
1 warning
```

Affected Company:

```text
SBIN
```

Dividend Payout:

```text
859%
```

---

## DQ-10 URL Validation

Result:

```text
1 warning
```

Affected Company:

```text
TVSMOTOR
```

Missing website URL.

---

# Audit Logging

Generated File:

`output/load_audit.csv`

Contents:

- Source rows
- Loaded rows
- Rejected rows

for all loaded tables.

---

# Validation Reporting

Generated File:

`output/validation_failures.csv`

Contains:

- Rule ID
- Severity
- Company
- Year
- Validation message

---

# Automated Testing

Framework:

`pytest`

Results:

```text
37 Passed
0 Failed
```

Breakdown:

| Test Suite | Count |
|------------|-------:|
| normalize_ticker | 15 |
| normalize_year | 20 |
| validator | 2 |
| Total | 37 |

Result:

```text
PASS
```

---

# Manual Review

Companies Reviewed:

- HDFCBANK
- RELIANCE
- TCS
- INFY
- SBIN

Checks Performed:

- Year coverage
- Duplicate years
- Missing values
- Financial reasonableness

Result:

```text
PASS
```

No critical issues identified.

---

# Sprint Outcome

Sprint Goal Status:

```text
COMPLETED
```

Achievements:

- ETL pipeline implemented
- SQLite schema deployed
- 11 tables loaded
- Data quality validation completed
- Audit logging implemented
- Automated tests passing
- Foreign key integrity verified

---

# Sprint Metrics

| Metric | Value |
|----------|--------|
| Tables Loaded | 11 |
| Companies | 92 |
| Stock Price Records | 5520 |
| DQ Rules Implemented | 10 |
| Unit Tests | 37 |
| FK Violations Remaining | 0 |
| Critical Failures | 0 |

---

## Sprint 1 Status

```text
COMPLETED
```

Story Points Delivered:

```text
34 / 34
```