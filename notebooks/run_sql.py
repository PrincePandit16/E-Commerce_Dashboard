import pandas as pd
import sqlite3

df = pd.read_csv('../data/clean_data.csv')  # use clean_data, not data.csv

conn = sqlite3.connect(':memory:')  # fixed typo: was :memeory:
df.to_sql('orders', conn, index=False, if_exists='replace')

total_revenue = pd.read_sql_query("""
    SELECT ROUND(SUM(Revenue), 2) AS total_revenue
    FROM orders""", conn)  # fixed: Revenue not REVENUE

aov = pd.read_sql_query("""
    SELECT ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2) AS avg_order_value
    FROM orders""", conn)

monthly = pd.read_sql_query("""
    SELECT YearMonth,
           ROUND(SUM(Revenue), 2)          AS monthly_revenue,
           COUNT(DISTINCT InvoiceNo)        AS total_orders,
           COUNT(DISTINCT CustomerID)       AS unique_customers
    FROM orders
    GROUP BY YearMonth
    ORDER BY YearMonth""", conn)  # fixed: added missing commas

top_products = pd.read_sql_query("""
    SELECT Description,
           ROUND(SUM(Revenue), 2) AS revenue,
           SUM(Quantity)          AS units_sold
    FROM orders
    GROUP BY Description
    ORDER BY revenue DESC
    LIMIT 10""", conn)

print("--- Total Revenue ---")
print(total_revenue)

print("\n--- Average Order Value ---")
print(aov)

print("\n--- Monthly Revenue ---")
print(monthly)

print("\n--- Top 10 Products ---")
print(top_products)

monthly.to_csv('../data/monthly_kpis.csv', index=False)
top_products.to_csv('../data/top_products.csv', index=False)

conn.close()
print("\nDone! CSVs saved.")