## 🛒 Retail Data Pipeline Project

A simulated end-to-end retail data pipeline project using Python, PostgreSQL, and FakeStoreAPI. This project ingests data daily, stores it in a PostgreSQL database, and generates visual analytics in Jupyter Notebook.

---

## 📦 Project Overview

This project simulates a small e-commerce store. The goal is to:
- Ingest fake retail data daily (products, users, carts)
- Store and manage the data using PostgreSQL
- Analyze sales trends and customer behavior
- Visualize key business insights in a Jupyter Notebook

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| 🐍 Python | Scripting, ingestion, analysis |
| 🐘 PostgreSQL | Relational database |
| 📦 FakeStoreAPI | Simulated retail data |
| 📊 Jupyter Notebook | Visualization and exploration |
| 🧮 SQL (Materialized Views) | Aggregation and analytics |
| 🧰 VS Code | Development environment |
| 📅 Windows Task Scheduler | Automate daily ingestion |

---

## 📁 Project Structure

retail-data-pipeline/
├── data_ingest/ # Python scripts for data ingestion
│ ├── fetch_initial_data.py
│ └── fetch_daily_data.py
├── notebooks/ # Jupyter notebook analysis
│ └── retail_analysis.ipynb
├── sql/ # SQL scripts for views
│ ├── create_tables.sql
│ ├── materialized_views.sql
├── logs/ # (Optional) Ingestion logs
├── analytics/ # (Optional) Final reports
├── .gitignore
├── requirements.txt
└── README.md

---

## 🚀 Step-by-Step Guide

---

### 🧩 Phase 1: Initial Setup


### ✅ Install Python, PostgreSQL, and VS Code  
### ✅ Create and activate a virtual environment


python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

### ✅ Connect VS Code to GitHub repo
### ✅ Create database in PostgreSQL: retail_data_pipeline


### 🔄 Phase 2: Data Ingestion


### 📦 Initial Load Script:

python data_ingest/fetch_initial_data.py

### 📅 Daily Fetch Script:

python data_ingest/fetch_daily_data.py

### 📁 Optionally run via .bat file and Windows Task Scheduler.


### 🗃️ Phase 3: Database Structure

### 🧱 Create tables:

products

users

carts

cart_items

### 🧠 Add Materialized Views:

top_products_mv

daily_revenue_mv

top_users_mv

Refresh them when data changes:

REFRESH MATERIALIZED VIEW top_products_mv;
REFRESH MATERIALIZED VIEW daily_revenue_mv;
REFRESH MATERIALIZED VIEW top_users_mv;


### 📊 Phase 4: Data Analysis


### 📁 In notebooks/retail_analysis.ipynb, visualize:

### 🏆 Top-Selling Products

### 📈 Daily Revenue Trends

### 🙋‍♂️ Most Loyal Users

### 📍 Example: Top products chart

sns.barplot(data=df_top_products, y="title", x="total_sold")
All queries pull data from materialized views to ensure performance.

### 📅 Automation

Set fetch_daily_data.py to run every day at 14:00 via Windows Task Scheduler or cron.


### 🤝 Contributing

This is a personal learning project — but PRs and suggestions are welcome!

### 📄 License

MIT License

### 🙌 Credits

FakeStoreAPI for fake retail data

PostgreSQL for DB magic

Matplotlib & Seaborn for visual storytelling
