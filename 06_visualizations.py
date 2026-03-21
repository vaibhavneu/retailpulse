import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sqlite3

conn = sqlite3.connect('retailpulse.db')
df = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
rfm = pd.read_csv('rfm_segments.csv')
cohort = pd.read_csv('cohort_retention.csv', index_col=0)

# Chart style
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f8f8'
plt.rcParams['font.family'] = 'sans-serif'

# ── CHART 1: Monthly Revenue ──────────────────────
df['month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
monthly = df.groupby('month')['Revenue'].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(monthly['month'], monthly['Revenue'], color='#4C72B0', edgecolor='white')
ax.set_title('Monthly Revenue — 2009 to 2010', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue (£)', fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('chart_01_monthly_revenue.png', dpi=150)
plt.close()
print("Chart 1 saved")

# ── CHART 2: Top 10 Products ──────────────────────
top_products = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)
top_products = top_products[~top_products.index.isin(['Manual', 'POSTAGE'])]

fig, ax = plt.subplots(figsize=(12, 6))
top_products.sort_values().plot(kind='barh', ax=ax, color='#55A868', edgecolor='white')
ax.set_title('Top 10 Products by Revenue', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Revenue (£)', fontsize=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
plt.tight_layout()
plt.savefig('chart_02_top_products.png', dpi=150)
plt.close()
print("Chart 2 saved")

# ── CHART 3: Revenue by Country ───────────────────
country_rev = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(8)

fig, ax = plt.subplots(figsize=(10, 5))
country_rev.plot(kind='bar', ax=ax, color='#C44E52', edgecolor='white')
ax.set_title('Revenue by Country — Top 8', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Country', fontsize=12)
ax.set_ylabel('Revenue (£)', fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('chart_03_revenue_by_country.png', dpi=150)
plt.close()
print("Chart 3 saved")

# ── CHART 4: RFM Segments ─────────────────────────
segment_counts = rfm['segment'].value_counts()
colors = ['#2ecc71','#3498db','#9b59b6','#f39c12','#e74c3c','#95a5a6']

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    segment_counts,
    labels=segment_counts.index,
    autopct='%1.1f%%',
    colors=colors,
    startangle=140,
    pctdistance=0.82
)
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')
ax.set_title('Customer Segments — RFM Analysis', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('chart_04_rfm_segments.png', dpi=150)
plt.close()
print("Chart 4 saved")

# ── CHART 5: Cohort Retention Heatmap ────────────
import seaborn as sns

cohort.index = cohort.index.astype(str)
cohort.columns = cohort.columns.astype(str)

fig, ax = plt.subplots(figsize=(14, 7))
sns.heatmap(
    cohort,
    annot=True,
    fmt='.0f',
    cmap='YlGnBu',
    ax=ax,
    linewidths=0.5,
    cbar_kws={'label': 'Retention %'}
)
ax.set_title('Cohort Retention Heatmap (%)', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Months Since First Purchase', fontsize=12)
ax.set_ylabel('Cohort Month', fontsize=12)
plt.tight_layout()
plt.savefig('chart_05_cohort_retention.png', dpi=150)
plt.close()
print("Chart 5 saved")

print("\nAll 5 charts saved successfully!")