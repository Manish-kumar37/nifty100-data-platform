-- SQLite
SELECT COUNT(*)
FROM financial_ratios;

SELECT
company_id,
year,
net_profit_margin_pct,
return_on_equity_pct,
debt_to_equity,
interest_coverage,
free_cash_flow_cr,
revenue_cagr_5yr,
pat_cagr_5yr,
eps_cagr_5yr
FROM financial_ratios
LIMIT 10;

SELECT *
FROM financial_ratios
WHERE company_id IN (
    'TCS',
    'INFY',
    'HDFCBANK',
    'RELIANCE',
    'ABB'
);

SELECT
    company_id,
    year,
    return_on_equity_pct,
    debt_to_equity
FROM financial_ratios
WHERE
    return_on_equity_pct > 15
    AND debt_to_equity < 1
ORDER BY return_on_equity_pct DESC;