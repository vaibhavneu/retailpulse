
import pandas as pd

print("Loading dataset...")
df = pd.read_excel('online_retail_II.xlsx', sheet_name='Year 2009-2010')
print(f"Raw data shape: {df.shape}")

# Step 1: Remove cancelled orders
df = df[~df['Invoice'].astype(str).str.startswith('C')]
print(f"After removing cancellations: {df.shape}")

# Step 2: Remove rows with missing Customer ID
df_customers = df.dropna(subset=['Customer ID'])
print(f"After removing missing Customer IDs: {df_customers.shape}")

# Step 3: Remove bad quantity and price values
df_customers = df_customers[df_customers['Quantity'] > 0]
df_customers = df_customers[df_customers['Price'] > 0]
print(f"After removing bad quantity/price: {df_customers.shape}")

# Step 4: Create a revenue column
df_customers['Revenue'] = df_customers['Quantity'] * df_customers['Price']

# Step 5: Fix data types
df_customers['Customer ID'] = df_customers['Customer ID'].astype(int)
df_customers['InvoiceDate'] = pd.to_datetime(df_customers['InvoiceDate'])

# Final summary
print("\n--- CLEAN DATASET SUMMARY ---")
print(f"Total transactions: {df_customers.shape[0]:,}")
print(f"Total revenue: £{df_customers['Revenue'].sum():,.2f}")
print(f"Unique customers: {df_customers['Customer ID'].nunique():,}")
print(f"Unique products: {df_customers['StockCode'].nunique():,}")
print(f"Date range: {df_customers['InvoiceDate'].min()} to {df_customers['InvoiceDate'].max()}")

# Save cleaned data
df_customers.to_csv('cleaned_retail.csv', index=False)
print("\nCleaned data saved to cleaned_retail.csv") 