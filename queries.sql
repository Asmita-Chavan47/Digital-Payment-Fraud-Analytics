USE fraud_detection;

SHOW TABLES;

-- Data Quality Check
SELECT COUNT(*) - COUNT(Amount) AS null_amount FROM transactions;
SELECT COUNT(*) AS total_transactions,
sum(Class = 1) as fraud_transactions,
sum(Class = 0) as normal_transactions
from transactions;

-- Q1: What is the total number of transactions in the dataset?
SELECT COUNT(*) AS total FROM transactions;

-- Q2: How many fraudulent vs legitimate transactions are there (Class distribution)?
SELECT Class, COUNT(*) as total FROM transactions GROUP BY Class;

-- Q3: What is the average and maximum transaction amount for fraud vs non-fraud?
SELECT Class, ROUND(AVG(Amount),2) AS avg_amount, MAX(Amount) AS max_amount FROM transactions GROUP BY Class;


-- Q4: What are the top 10 highest-value fraudulent transactions?
SELECT Time, Amount, V14, V17, Class 
FROM transactions 
WHERE Class = 1 
ORDER BY Amount DESC 
LIMIT 10;

-- Q5: How many transactions have amount above 100,500 and 1000
SELECT 
  SUM(CASE WHEN Amount > 100 THEN 1 ELSE 0 END) AS fraud_above_100,
  SUM(CASE WHEN Amount > 500 THEN 1 ELSE 0 END) AS fraud_above_500,
  SUM(CASE WHEN Amount > 1000 THEN 1 ELSE 0 END) AS fraud_above_1000
FROM transactions WHERE Class = 1;

-- Q6: How does the fraud rate vary by transaction hour (Time-based fraud trend)?
SELECT
    FLOOR(`Time` / 3600) AS elapsed_hour_bucket,
    COUNT(*) AS total_transactions,
    SUM(Class = 1) AS fraud_count,
    ROUND(
        100.0 * SUM(Class = 1) / COUNT(*),
        4
    ) AS fraud_rate_percent
FROM transactions
GROUP BY FLOOR(`Time` / 3600)
ORDER BY elapsed_hour_bucket;


-- Q7: Evaluate suspicious transaction rule using precision and recall?
SELECT
    COUNT(*) AS suspicious_transactions,
    SUM(Class = 1) AS actual_fraud,
    SUM(Class = 0) AS normal_flagged,
    ROUND(
        100.0 * SUM(Class = 1) / COUNT(*),
        2
    ) AS precision_percent,
    ROUND(
        100.0 * SUM(Class = 1) /
        (SELECT COUNT(*) FROM transactions WHERE Class = 1),
        2
    ) AS fraud_recall_percent
FROM transactions
WHERE V14 < -5 AND Amount > 100;

-- Q8: What is the average value of key risk features for fraud vs non-fraud transactions?
SELECT 
  Class,
  COUNT(*) AS total,
  ROUND(AVG(V12),2) AS V12_avg,
  ROUND(AVG(V14),2) AS V14_avg,
  ROUND(AVG(V17),2) AS V17_avg,
  ROUND(AVG(Amount),2) AS Amount_avg
FROM transactions 
GROUP BY Class;

-- Q9: What is the fraud rate across different transaction amount ranges?
SELECT
    CASE
        WHEN Amount < 50 THEN '0-Under 50'
        WHEN Amount < 100 THEN '50-Under 100'
        WHEN Amount < 500 THEN '100-Under 500'
        ELSE '500 and above'
    END AS amount_range,
    COUNT(*) AS total_transactions,
    SUM(Class = 1) AS fraud_count,
    ROUND(
        100.0 * SUM(Class = 1) / COUNT(*),
        4
    ) AS fraud_rate_percent
FROM transactions
WHERE Amount >= 0
GROUP BY
    CASE
        WHEN Amount < 50 THEN '0-Under 50'
        WHEN Amount < 100 THEN '50-Under 100'
        WHEN Amount < 500 THEN '100-Under 500'
        ELSE '500 and above'
    END
ORDER BY fraud_rate_percent DESC;

