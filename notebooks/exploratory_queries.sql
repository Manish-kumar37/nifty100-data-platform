-- 1
SELECT COUNT(*) FROM companies;

-- 2
SELECT COUNT(*) FROM profitandloss;

-- 3
SELECT COUNT(*) FROM balancesheet;

-- 4
SELECT COUNT(*) FROM cashflow;

-- 5
SELECT company_id,
       MAX(net_profit) AS max_profit
FROM profitandloss
GROUP BY company_id
ORDER BY max_profit DESC
LIMIT 10;

-- 6
SELECT company_id,
       MAX(roe_percentage) AS roe
FROM companies
GROUP BY company_id
ORDER BY roe DESC
LIMIT 10;

-- 7
SELECT company_id,
       COUNT(*) AS years_available
FROM profitandloss
GROUP BY company_id
ORDER BY years_available ASC
LIMIT 10;

-- 8
SELECT broad_sector,
       COUNT(*) AS companies
FROM sectors
GROUP BY broad_sector
ORDER BY companies DESC;

-- 9
SELECT company_id,
       AVG(close_price) AS avg_price
FROM stock_prices
GROUP BY company_id
ORDER BY avg_price DESC
LIMIT 10;

-- 10
SELECT *
FROM load_audit;
--for manual check 5 companies 
SELECT *
FROM profitandloss
WHERE company_id='HDFCBANK';

SELECT *
FROM profitandloss
WHERE company_id='RELIANCE';

SELECT *
FROM profitandloss
WHERE company_id='TCS';

SELECT *
FROM profitandloss
WHERE company_id='INFY';

SELECT *
FROM profitandloss
WHERE company_id='SBIN';