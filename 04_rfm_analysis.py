import pandas as pd
import sqlite3

conn = sqlite3.connect('retailpulse.db')
df = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

# Convert date column
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Reference date - the day after the last transaction
# This is used to calculate how many days ago each customer last bought
reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

print(f"Reference date: {reference_date.date()}")

# --- Build RFM table ---
# For each customer, calculate R, F, and M
rfm = df.groupby('Customer ID').agg(
    last_purchase=('InvoiceDate', 'max'),
    frequency=('Invoice', 'nunique'),
    monetary=('Revenue', 'sum')
).reset_index()

# Recency = how many days since last purchase
rfm['recency'] = (reference_date - rfm['last_purchase']).dt.days

# --- Score each customer 1 to 4 ---
# For recency: lower days = better = higher score
rfm['R_score'] = pd.qcut(rfm['recency'], q=4, labels=[4, 3, 2, 1])
# For frequency and monetary: higher = better = higher score
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
rfm['M_score'] = pd.qcut(rfm['monetary'], q=4, labels=[1, 2, 3, 4])

# Combine scores into one RFM score
rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

# --- Assign segments based on scores ---
def assign_segment(row):
    r = int(row['R_score'])
    f = int(row['F_score'])
    m = int(row['M_score'])
    if r >= 3 and f >= 3 and m >= 3:
        return 'Champion'
    elif r >= 3 and f >= 2:
        return 'Loyal'
    elif r >= 2 and f >= 2:
        return 'Potential Loyalist'
    elif r >= 3 and f <= 2:
        return 'New Customer'
    elif r == 2 and f <= 2:
        return 'At Risk'
    else:
        return 'Lost'

rfm['segment'] = rfm.apply(assign_segment, axis=1)

# --- Print results ---
print("\n--- RFM SEGMENT SUMMARY ---")
segment_summary = rfm.groupby('segment').agg(
    customer_count=('Customer ID', 'count'),
    avg_recency=('recency', 'mean'),
    avg_frequency=('frequency', 'mean'),
    avg_monetary=('monetary', 'mean')
).round(1).sort_values('customer_count', ascending=False)

print(segment_summary.to_string())

# Save RFM results
rfm.to_csv('rfm_segments.csv', index=False)
print("\nRFM data saved to rfm_segments.csv")