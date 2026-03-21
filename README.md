# RetailPulse — E-commerce Analytics Project

An end-to-end data analytics project analysing 500K+ transactions from a UK-based online retailer (Dec 2009 – Dec 2010).

## Live Dashboard
[View Interactive Dashboard](https://vaibhavneu.github.io/retailpulse/dashboard.html)

## Project Overview
This project simulates a real-world analyst workflow — from raw data to business insights and recommendations.

**Dataset:** UCI Online Retail II — 525,461 transactions, 8 columns  
**Tools:** Python, SQL (SQLite), Tableau, HTML/CSS/JavaScript  
**Libraries:** pandas, matplotlib, seaborn, sqlalchemy

## Key Findings
- **£8.83M** total revenue across 407,664 transactions
- **Strong seasonality** — Q4 revenue nearly double Q1/Q2, driven by gift purchasing
- **29.9% Champion customers** generating avg £4,970 each — top retention priority
- **25% Lost customers** — significant win-back opportunity worth investigating
- **UK accounts for 83.95%** of revenue — international markets remain underpenetrated

## Project Structure
```
retailpulse/
├── 01_cleaning.py          # Data cleaning
├── 02_load_to_db.py        # Loads to SQLite
├── 03_sql_analysis.py      # SQL queries
├── 04_rfm_analysis.py      # RFM segmentation
├── 05_cohort_analysis.py   # Cohort retention
├── 06_visualizations.py    # Charts
└── dashboard.html          # Web dashboard
```

## Analysis Modules

### 1. Data Cleaning
- Removed 10,206 cancelled orders
- Removed 107,927 rows with missing Customer IDs
- Created Revenue column (Quantity x Price)
- Final clean dataset: 407,664 rows

### 2. SQL Analysis
- Monthly revenue trends
- Top 10 products by revenue
- Revenue by country with percentage share

### 3. RFM Customer Segmentation

| Segment | Customers | Avg Spend |
|---|---|---|
| Champion | 1,288 | £4,970 |
| Loyal | 603 | £586 |
| Potential Loyalist | 782 | £1,488 |
| New Customer | 299 | £361 |
| At Risk | 264 | £435 |
| Lost | 1,076 | £642 |

### 4. Cohort Retention Analysis
- Tracked 13 monthly cohorts
- Average Month 1 retention: 20–35%
- December 2009 cohort strongest — 49.5% retention at Month 11

## Business Recommendations
1. **Retain Champions** — launch loyalty programme for 1,288 Champion customers
2. **Win back Lost customers** — targeted reactivation campaign with discount incentive
3. **Improve new customer onboarding** — welcome series for new customers
4. **Double down on Q4** — higher inventory and marketing budget for Oct–Nov peak
5. **Expand internationally** — EIRE and Netherlands show strong revenue potential

## Author
**Vaibhav Viraj** — Data Analyst  
[GitHub](https://github.com/vaibhavneu)
```

