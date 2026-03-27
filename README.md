# 🛒 E-Commerce Sales Intelligence Dashboard

> A complete end-to-end data analytics project — from raw transactional data to an interactive business dashboard with sales forecasting.

![Python](https://img.shields.io/badge/Python-3.10.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-red?style=flat-square&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.24.1-blue?style=flat-square&logo=plotly)
![Prophet](https://img.shields.io/badge/Prophet-Forecasting-orange?style=flat-square)
![SQLite](https://img.shields.io/badge/SQL-SQLite-lightgrey?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Project Objective

Analyze a real-world UK e-commerce dataset to extract actionable business insights and present them through an interactive, filterable dashboard — covering sales trends, product performance, customer behaviour, and a 90-day revenue forecast.

---

## 📊 Dataset

| Property | Detail |
|---|---|
| Source | [UCI Online Retail Dataset via Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data) |
| Period | December 2010 – December 2011 |
| Raw Records | 541,909 rows |
| Clean Records | 397,884 rows (after cleaning) |
| Columns | InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country |

> **Note:** The full dataset is not included in this repo due to size. Download it from the Kaggle link above and place it at `data/data.csv`.

---

## 🗂️ Project Structure

```
ecommerce-dashboard/
│
├── data/
│   ├── data.csv                  ← raw dataset (download from Kaggle)
│   ├── clean_data.csv            ← generated after running analysis.ipynb
│   ├── monthly_kpis.csv          ← generated after running run_sql.py
│   ├── top_products.csv          ← generated after running run_sql.py
│   ├── forecast_plot.png         ← generated after running forecast.py
│   └── forecast_components.png  ← generated after running forecast.py
│
├── notebooks/
│   ├── analysis.ipynb            ← data cleaning and EDA
│   └── run_sql.py                ← SQL KPI queries via SQLite
│
├── sql/
│   └── queries.sql               ← all SQL queries documented
│
├── dashboard/
│   └── app.py                    ← Streamlit dashboard
│
├── models/
│   └── forecast.py               ← Prophet sales forecasting model
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10.11
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/PrincePandit16/ecommerce-dashboard.git
cd ecommerce-dashboard
```

### Step 2 — Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Download the dataset
Download `data.csv` from [Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data) and place it inside the `data/` folder.

---

## 🚀 How to Run

Run the files **in this exact order**:

### 1. Data Cleaning (Jupyter Notebook)
```bash
cd notebooks
jupyter notebook
```
Open `analysis.ipynb` and click **Run All Cells**.
This generates `data/clean_data.csv`.

### 2. SQL KPI Analysis
```bash
cd notebooks
python run_sql.py
```
This generates `data/monthly_kpis.csv` and `data/top_products.csv`.

### 3. Sales Forecast Model
```bash
cd models
python forecast.py
```
This generates `data/forecast_plot.png` and `data/forecast_components.png`.

### 4. Launch the Dashboard
```bash
cd dashboard
streamlit run app.py
```
Opens the dashboard at `http://localhost:8501`

---

## 🧹 Data Cleaning Approach

| Step | Action | Reason |
|---|---|---|
| 1 | Drop rows with missing `CustomerID` | Cannot track customer behaviour without an ID |
| 2 | Remove cancelled orders (`InvoiceNo` starting with 'C') | Cancellations distort revenue figures |
| 3 | Remove rows where `Quantity` ≤ 0 or `UnitPrice` ≤ 0 | Data entry errors / returns |
| 4 | Convert `InvoiceDate` from string to datetime | Required for time-series analysis |
| 5 | Create `Revenue` column (`Quantity × UnitPrice`) | Core metric for all KPIs |
| 6 | Add `YearMonth` column | Enables monthly grouping in SQL and charts |
| 7 | Remove duplicate rows | Prevents double-counting |

**Result:** 541,909 → 397,884 rows (clean, reliable data)

---

## 🗄️ SQL KPIs

All queries are in `sql/queries.sql` and executed via SQLite in Python.

| KPI | SQL Technique Used |
|---|---|
| Total Revenue | `SUM(Revenue)` |
| Average Order Value (AOV) | `SUM(Revenue) / COUNT(DISTINCT InvoiceNo)` |
| Monthly Revenue & Growth | CTE + `LAG()` window function |
| Customer Retention Rate | Self-join on monthly customer table |
| Top 10 Products | `GROUP BY` + `ORDER BY revenue DESC` |

> **Why `COUNT(DISTINCT InvoiceNo)` for AOV?** Each order has multiple rows (one per product). Using `COUNT(*)` would divide by line items, not orders — giving a wrong, much smaller AOV.

---

## 📈 Dashboard Features

Built with **Streamlit** + **Plotly**. Launch with `streamlit run dashboard/app.py`.

| Tab | Content |
|---|---|
| 📈 Sales Trends | Monthly revenue line chart + growth % table |
| 🏆 Top Products | Top 10 products horizontal bar chart by revenue |
| 👥 Customer Insights | Repeat rate metric, order distribution histogram, top spenders table |
| 🔮 Sales Forecast | Prophet 90-day forecast chart + seasonality components |

**Sidebar filters:** Date range picker + Country selector — both filter all tabs simultaneously.

---

## 🔮 Sales Forecasting Model

- **Library:** Facebook Prophet (Meta)
- **Approach:** Daily revenue aggregation → train/test split (last 30 days as test) → 90-day forecast
- **Seasonality:** Weekly (`weekly_seasonality=True`), Yearly (`yearly_seasonality='auto'`)
- **Accuracy Metric:** MAPE (Mean Absolute Percentage Error)
- **Output:** Forecast chart + components chart (trend, weekly seasonality)

---

## 💡 Key Business Insights

### 1. Revenue is highly concentrated in a few products
The top 10 products drive a disproportionate share of total revenue. Bundling high-performing SKUs with slower-moving products could lift Average Order Value significantly.

### 2. Customer retention drops sharply after month 1
Only ~35% of customers return after their first purchase. A targeted re-engagement email campaign at day 30–45 post-purchase could recover 10–15% of churned customers and improve lifetime value.

### 3. November is the peak revenue month
Sales spike sharply in November due to Christmas gift buying. Inventory and marketing budgets should be scaled up by mid-October to fully capitalise on this seasonal demand.

### 4. The UK accounts for 80%+ of all revenue
International markets (Germany, France, Netherlands) are present but significantly under-served. These represent a clear, low-risk international expansion opportunity.

### 5. Weekend sales are consistently lower
Transaction volume drops ~40% on Saturdays and Sundays compared to weekdays. Scheduled weekend promotions or email campaigns could recover meaningful revenue from this dip.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10.11 | Core language |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical operations |
| SQLite (via Python) | SQL KPI queries on CSV data |
| Streamlit | Interactive web dashboard |
| Plotly | Interactive charts |
| Facebook Prophet | Time-series sales forecasting |
| Scikit-learn | MAPE accuracy metric |
| Matplotlib | Forecast plot rendering |
| Jupyter Notebook | Exploratory data analysis |

---

## 📋 Requirements

```
pandas==2.2.3
numpy==1.26.4
matplotlib==3.9.4
seaborn==0.13.2
streamlit==1.45.1
plotly==5.24.1
openpyxl==3.1.5
scikit-learn==1.6.1
jupyter==1.1.1
prophet
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🙋 Approach Summary

1. **Started with understanding the data** — explored shape, dtypes, nulls, and value distributions before writing a single line of cleaning code.
2. **Cleaned with business logic** — every cleaning decision was driven by what would corrupt downstream analysis, not just what looked "messy".
3. **Used real SQL** — loaded the dataframe into SQLite to write and demonstrate proper SQL queries with CTEs and window functions.
4. **Built a multi-tab dashboard** — organised insights into logical sections a business stakeholder would care about.
5. **Added forecasting as a bonus** — used Prophet for its ability to handle seasonality automatically, which is critical for retail data.
6. **Focused on actionable insights** — every insight includes a specific business recommendation, not just an observation.

---


