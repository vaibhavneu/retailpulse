import pandas as pd
import sqlite3

conn = sqlite3.connect('retailpulse.db')

print("=" * 50)
print("QUESTION 1: What is our monthly revenue?")
print("=" * 50)

query1 = """
SELECT 
    strftime('%Y-%m', InvoiceDate) AS month,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    COUNT(DISTINCT Invoice) AS total_orders,
    COUNT(DISTINCT "Customer ID") AS unique_customers
FROM transactions
GROUP BY month
ORDER BY month
"""

q1 = pd.read_sql(query1, conn)
print(q1.to_string(index=False))

print("\n" + "=" * 50)
print("QUESTION 2: What are our top 10 products?")
print("=" * 50)

query2 = """
SELECT 
    Description AS product,
    SUM(Quantity) AS total_units_sold,
    ROUND(SUM(Revenue), 2) AS total_revenue
FROM transactions
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 10
"""

q2 = pd.read_sql(query2, conn)
print(q2.to_string(index=False))

print("\n" + "=" * 50)
print("QUESTION 3: Which countries generate the most revenue?")
print("=" * 50)

query3 = """
SELECT 
    Country,
    COUNT(DISTINCT "Customer ID") AS customers,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(SUM(Revenue) * 100.0 / (SELECT SUM(Revenue) FROM transactions), 2) AS revenue_pct
FROM transactions
GROUP BY Country
ORDER BY total_revenue DESC
LIMIT 10
"""

q3 = pd.read_sql(query3, conn)
print(q3.to_string(index=False))

conn.close()