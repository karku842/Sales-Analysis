# 📊 Retail Sales Analysis | End-to-End Data Analytics Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow)
![Pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458)
![Status](https://img.shields.io/badge/Status-Complete-green)

## 📌 Project Overview
This project is a complete **end-to-end analytics pipeline** built to analyze retail sales performance, identify revenue drivers, uncover customer behavior, and quantify revenue leakage due to cancellations and returns.

It follows a complete lifecycle:
**Raw Data** $\rightarrow$ **Cleaning** $\rightarrow$ **Feature Engineering** $\rightarrow$ **Analysis** $\rightarrow$ **Data Modeling** $\rightarrow$ **Power BI Dashboard** $\rightarrow$ **Executive Insights Report**

The final output is a polished, business-ready analytics system that transforms raw transaction logs into actionable strategic insights.

---

## 🔍 Project Objectives
- **Build a clean and reliable dataset** for analysis.
- **Generate reusable analytical tables** optimized for Power BI.
- **Understand sales behavior** across time, customers, products, and countries.
- **Identify high-performing categories and products.**
- **Detect revenue leakage** from cancellations and returns.
- **Develop a professional Power BI dashboard.**
- **Produce an executive-level analytic report.**

> *This project showcases real-world skills required for Data Analyst / BI Analyst roles, including ETL, modeling, and storytelling.*

---

## 🛠️ Tech Stack
- **Python:** Data cleaning, feature engineering, and preprocessing (Pandas, NumPy).
- **Power BI:** Data visualization, DAX measures, and interactive dashboarding.
- **Data Modeling:** Star Schema design.
- **Documentation:** Markdown & Business Reporting.

---

## 🧼 1. Data Cleaning & Feature Engineering
The raw dataset (`Da_Cleaned.csv`) was processed using Python to create a robust foundation for analysis:

- **Timestamp Conversion:** Converted strings to datetime objects.
- **Calendar Features:** Generated `Year`, `Month`, `Quarter`, `Weekday`, and `Hour` columns.
- **Status Normalization:** Standardized categories into `Delivered`, `Cancelled`, and `Returned`.
- **Leakage Metrics:** Created specific features for `LostOnCancels` and `LostOnReturns`.
- **Naming Conventions:** Standardized column names for the FactSales table.

---

## 📦 2. Sales Analysis Pipeline (Python)
A reusable Python script exports all necessary analytical tables to the `pbix_outputs/` folder for direct Power BI ingestion:

| Table | Description |
| :--- | :--- |
| **KPI Summary** | Aggregated high-level metrics. |
| **Sales Trends** | Monthly, weekly, and hourly breakdowns. |
| **Category/Product** | Top performers and contribution analysis. |
| **Customer Data** | Spend behavior, frequency, and value. |
| **Country Perf** | Geographic sales distribution. |
| **Leakage Analysis** | Detailed cancellation and return metrics. |

---

## 🧠 3. Data Modeling (Star Schema)
To ensure optimized performance in Power BI, a **Star Schema** was implemented:

- **Fact Table:** `FactSales` (Transaction-level data)
- **Dimension Tables:**
  - `DimDate`
  - `DimCustomer`
  - `DimProduct`
  - `DimCategory`
  - `DimCountry`
  - `DimStatus`

*Relationships are single-direction, many-to-one, ensuring clean and efficient DAX calculations.*

---

## 📊 4. Power BI Dashboard Structure
The dashboard consists of 5 focused pages:

1.  **Executive Overview:** High-level KPIs (Gross Revenue, Net Revenue, Leakage), trend lines, and insight summaries.
2.  **Sales Over Time:** Seasonal trends, weekday performance, and peak hourly analysis.
3.  **Category & Product:** Deep dive into top categories, sub-categories, and best-selling SKUs.
4.  **Customer Insights:** Top customer ranking, spend distribution, and churn indicators.
5.  **Revenue Leakage:** Analysis of lost revenue by category, product, and return reasons.

---

## 📈 5. Key Business Insights
- **Revenue Overview:**
  - **Gross Revenue:** ₹95.35L
  - **Net Delivered Revenue:** ₹89.24L
  - **Leakage:** ₹6.11L (6.41% lost to returns/cancellations).
- **Seasonality:** Peak sales occurred in **September**, with Q4 consistently driving the most revenue.
- **Operational Patterns:**
  - **Best Day:** Thursday.
  - **Peak Hour:** 12:00 PM.
- **Top Products:** *Paper Craft – Little Birdie*, *Regency Cakestand*, and *White Hanging Heart T-Light Holder*.
- **Customer Base:** ~4,000 unique customers with an Average Order Value (AOV) of **₹402.18**.

---

## 🚀 6. What This Project Demonstrates
✅ **Data Cleaning:** Handling raw, messy data and creating meaningful features.
✅ **Pipeline Building:** Automating the flow from raw CSV to analytical tables.
✅ **Dimensional Modeling:** Designing efficient Star Schemas.
✅ **Visualization:** Creating intuitive Power BI dashboards.
✅ **Business Acumen:** Translating data into strategic executive reports.

---

## 📌 7. Future Enhancements
- [ ] **RFM Segmentation Model:** Automating customer tiering (Champions, Hibernating, etc.).
- [ ] **Cohort Analysis:** Tracking customer retention over time.
- [ ] **Forecasting:** Implementing time-series forecasting for inventory planning.

---

## 💡 Conclusion
This project provides a complete analytics ecosystem — from raw data to boardroom insights. It demonstrates the ability to **prepare data, build pipelines, model effectively, visualize intelligently, and produce actionable business insights.**

---

### 📬 Author
*Karghuvel Rajan.G / www.linkedin.com/in/karghuvel-rajan-g*
