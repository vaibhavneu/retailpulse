import pandas as pd
import sqlite3

conn = sqlite3.connect('retailpulse.db')
df = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

# Convert date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Step 1: Find each customer's first purchase month
# This defines which cohort they belong to
df['month'] = df['InvoiceDate'].dt.to_period('M')
first_purchase = df.groupby('Customer ID')['month'].min().reset_index()
first_purchase.columns = ['Customer ID', 'cohort_month']

# Step 2: Merge cohort month back into main dataframe
df = df.merge(first_purchase, on='Customer ID')

# Step 3: Calculate how many months after first purchase each transaction happened
df['cohort_index'] = (df['month'] - df['cohort_month']).apply(lambda x: x.n)

# Step 4: Count unique customers per cohort per month index
cohort_data = df.groupby(['cohort_month', 'cohort_index'])['Customer ID'].nunique().reset_index()
cohort_data.columns = ['cohort_month', 'cohort_index', 'customers']

# Step 5: Pivot into a table
cohort_pivot = cohort_data.pivot_table(
    index='cohort_month',
    columns='cohort_index',
    values='customers'
)

# Step 6: Convert to retention percentages
cohort_size = cohort_pivot[0]
retention = cohort_pivot.divide(cohort_size, axis=0).round(3) * 100

print("--- COHORT RETENTION TABLE (%) ---")
print(retention.to_string())

# Save
retention.to_csv('cohort_retention.csv')
print("\nCohort data saved to cohort_retention.csv")