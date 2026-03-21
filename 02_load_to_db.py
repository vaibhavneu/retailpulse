import pandas as pd
import sqlite3
print("Loading cleaned data...")
df = pd.read_csv('cleaned_retail.csv')
conn = sqlite3.connect('retailpulse.db')
df.to_sql('transactions', conn, if_exists='replace', index=False)
print(f"Loaded {len(df):,} rows into the database")
query = "SELECT COUNT(*) as total_rows FROM transactions"
result = pd.read_sql(query, conn)
print("Database check:", result)

conn.close()
print("\nDatabase saved as retailpulse.db")