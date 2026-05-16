import pandas as pd
import sqlite3

conn = sqlite3.connect('retailpulse.db')

print("=" * 50)
print("QUERY 4: Running Revenue by Month")
print("=" * 50)

query4 = """
WITH monthly AS (
    SELECT
        strftime('%Y-%m', InvoiceDate) AS month,
        ROUND(SUM(Revenue), 2) AS monthly_revenue
    FROM transactions
    GROUP BY strftime('%Y-%m', InvoiceDate)
)
SELECT
    month,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY month), 2) AS running_revenue
FROM monthly
ORDER BY month;
"""

q4 = pd.read_sql(query4, conn)
print(q4.to_string(index=False))


print("=" * 50)
print("QUERY 5: Top Product Per Country")
print("=" * 50)

query5 = """
WITH product_revenue AS (
    SELECT
        Country,
        Description,
        ROUND(SUM(Revenue), 2) AS total_revenue
    FROM transactions
    GROUP BY Country, Description
),
ranked AS (
    SELECT
        Country,
        Description,
        total_revenue,
        RANK() OVER (
            PARTITION BY Country
            ORDER BY total_revenue DESC
        ) AS revenue_rank
    FROM product_revenue
)
SELECT
    Country,
    Description,
    total_revenue
FROM ranked
WHERE revenue_rank = 1
ORDER BY total_revenue DESC;
"""

q5 = pd.read_sql(query5, conn)
print(q5.to_string(index=False))


print("=" * 50)
print("QUERY 6: Month-over-Month Revenue Growth")
print("=" * 50)

query6 = """
WITH monthly AS (
    SELECT
        strftime('%Y-%m', InvoiceDate) AS month,
        ROUND(SUM(Revenue), 2) AS monthly_revenue
    FROM transactions
    GROUP BY strftime('%Y-%m', InvoiceDate)
),
with_prev AS (
    SELECT
        month,
        monthly_revenue,
        LAG(monthly_revenue, 1) OVER (ORDER BY month) AS prev_revenue
    FROM monthly
)
SELECT
    month,
    monthly_revenue,
    prev_revenue,
    ROUND(
        ((monthly_revenue - prev_revenue) * 100.0 / prev_revenue),
        2
    ) AS mom_growth_pct
FROM with_prev
ORDER BY month;
"""

q6 = pd.read_sql(query6, conn)
print(q6.to_string(index=False))


print("=" * 50)
print("QUERY 7: RFM Customer Segmentation")
print("=" * 50)

query7 = """
WITH customer_rfm AS (
    SELECT
        "Customer ID",
        CAST(
            julianday((SELECT MAX(InvoiceDate) FROM transactions))
            - julianday(MAX(InvoiceDate))
            AS INTEGER
        ) AS recency,
        COUNT(DISTINCT Invoice) AS frequency,
        ROUND(SUM(Revenue), 2) AS monetary
    FROM transactions
    WHERE "Customer ID" IS NOT NULL
    GROUP BY "Customer ID"
),
rfm_scores AS (
    SELECT
        "Customer ID",
        recency,
        frequency,
        monetary,
        NTILE(4) OVER (ORDER BY recency DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM customer_rfm
),
segmented AS (
    SELECT
        "Customer ID",
        recency,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        (r_score + f_score + m_score) AS rfm_total_score,
        CASE
            WHEN r_score = 4 AND f_score = 4 AND m_score = 4 THEN 'Best Customers'
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
            WHEN r_score >= 3 AND f_score <= 2 THEN 'Recent Customers'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk Customers'
            WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost Customers'
            ELSE 'Regular Customers'
        END AS customer_segment
    FROM rfm_scores
)
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(recency), 2) AS avg_recency_days,
    ROUND(AVG(frequency), 2) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_monetary_value,
    ROUND(SUM(monetary), 2) AS total_revenue
FROM segmented
GROUP BY customer_segment
ORDER BY total_revenue DESC;
"""

q7 = pd.read_sql(query7, conn)
print(q7.to_string(index=False))


print("=" * 50)
print("QUERY 8: Customers Spending Above Country Average")
print("=" * 50)

query8 = """
WITH customer_spend AS (
    SELECT
        "Customer ID",
        Country,
        ROUND(SUM(Revenue), 2) AS total_spend
    FROM transactions
    WHERE "Customer ID" IS NOT NULL
    GROUP BY "Customer ID", Country
),
country_avg AS (
    SELECT
        Country,
        ROUND(AVG(total_spend), 2) AS avg_spend
    FROM customer_spend
    GROUP BY Country
)
SELECT
    c."Customer ID",
    c.Country,
    c.total_spend,
    a.avg_spend,
    ROUND(c.total_spend - a.avg_spend, 2) AS above_avg_by
FROM customer_spend c
JOIN country_avg a ON c.Country = a.Country
WHERE c.total_spend > a.avg_spend
ORDER BY c.total_spend DESC
LIMIT 20;
"""

q8 = pd.read_sql(query8, conn)
print(q8.to_string(index=False))
conn.close()