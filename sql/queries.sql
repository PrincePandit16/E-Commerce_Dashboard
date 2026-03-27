-- Total Revenue --
SELECT ROUND(SUM(Quantity * UnitPrice), 2) AS total_revenue
FROM orders;

-- Average Order Value (AOV) --
SELECT ROUND(SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo), 2) AS avg_order_value
FROM orders;

-- Monthly Revenue --
SELECT
    YearMonth,
    ROUND(SUM(Quantity * UnitPrice), 2) AS monthly_revenue,
    COUNT(DISTINCT InvoiceNo)           AS total_orders,
    COUNT(DISTINCT CustomerID)          AS unique_customers
FROM orders
GROUP BY YearMonth
ORDER BY YearMonth;

-- Monthly Sales Growth --
WITH monthly AS (
    SELECT YearMonth, SUM(Quantity * UnitPrice) AS revenue
    FROM orders
    GROUP BY YearMonth
)
SELECT
    YearMonth,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY YearMonth))
        * 100.0
        / LAG(revenue) OVER (ORDER BY YearMonth),
    2) AS growth_pct
FROM monthly;

-- Customer Retention Rate --
WITH monthly_customers AS (
    SELECT DISTINCT CustomerID, YearMonth FROM orders
),
retention AS (
    SELECT
        a.YearMonth,
        COUNT(DISTINCT b.CustomerID) AS retained,
        COUNT(DISTINCT a.CustomerID) AS total
    FROM monthly_customers a
    LEFT JOIN monthly_customers b
        ON a.CustomerID = b.CustomerID
       AND b.YearMonth = strftime('%Y-%m', date(a.YearMonth || '-01', '+1 month'))
    GROUP BY a.YearMonth
)
SELECT YearMonth, ROUND(100.0 * retained / total, 2) AS retention_rate_pct
FROM retention
ORDER BY YearMonth;

-- Top 10 Products by Revenue --
SELECT Description,
       ROUND(SUM(Quantity * UnitPrice), 2) AS revenue,
       SUM(Quantity) AS units_sold
FROM orders
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10;