import os
import pandas as pd
import numpy as np

# ========= 1. PATHS & SETUP =========
INPUT_PATH = "Da_Cleaned.csv"      # change if needed
OUTPUT_DIR = "pbix_outputs"        # folder for Power BI tables

os.makedirs(OUTPUT_DIR, exist_ok=True)

pd.set_option("display.max_columns", None)

# ========= 2. LOAD DATA =========
df = pd.read_csv(INPUT_PATH)

# ========= 3. BASIC CLEANING & FEATURE ENGINEERING =========

# Parse dates
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
df["DateTime"] = pd.to_datetime(
    df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Time"],
    errors="coerce"
)

# Standardize column names (optional but helpful)
df.columns = (
    df.columns
      .str.strip()
      .str.replace(" ", "_")
      .str.replace("-", "_")
)

# Calendar features
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
df["Weekday"] = df["Date"].dt.day_name()

# Hour feature from Time
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.hour

# Status normalization
df["Status"] = df["Status"].str.title()

delivered = df[df["Status"] == "Delivered"].copy()
cancelled = df[df["Status"] == "Cancelled"].copy()
returned  = df[df["Status"] == "Returned"].copy()

# ========= 4. KPI TABLE =========

date_min = df["Date"].min().date()
date_max = df["Date"].max().date()

total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_countries = df["Country"].nunique()

total_gross_sales = df["Gross_Sales"].sum()
total_delivered_sales = delivered["Sales"].sum()
total_lost_cancels = df["LostOnCancles"].sum()
total_lost_returns = df["LostOnReturns"].sum()
total_lost_revenue = total_lost_cancels + total_lost_returns

avg_order_value = total_delivered_sales / total_orders if total_orders else 0
loss_pct = (total_lost_revenue / total_gross_sales * 100) if total_gross_sales else 0

summary_kpis = pd.DataFrame([{
    "date_range_start": date_min,
    "date_range_end": date_max,
    "total_orders": total_orders,
    "unique_customers": total_customers,
    "countries": total_countries,
    "gross_sales_incl_lost": round(total_gross_sales, 2),
    "delivered_sales": round(total_delivered_sales, 2),
    "revenue_lost_cancels": round(total_lost_cancels, 2),
    "revenue_lost_returns": round(total_lost_returns, 2),
    "revenue_lost_total": round(total_lost_revenue, 2),
    "revenue_loss_pct_of_gross": round(loss_pct, 2),
    "avg_order_value_delivered": round(avg_order_value, 2)
}])

summary_kpis.to_csv(os.path.join(OUTPUT_DIR, "kpi_summary.csv"), index=False)

# ========= 5. TIME-BASED TABLES =========

# 5.1 Monthly sales (delivered only)
monthly_sales = (
    delivered
    .groupby("YearMonth", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "delivered_sales"})
    .sort_values("YearMonth")
)
monthly_sales.to_csv(os.path.join(OUTPUT_DIR, "monthly_sales.csv"), index=False)

# 5.2 Weekday sales
weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
weekday_sales = (
    delivered
    .groupby("Weekday", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "delivered_sales"})
)

# Ensure sorted by actual weekday order
weekday_sales["Weekday"] = pd.Categorical(weekday_sales["Weekday"], categories=weekday_order, ordered=True)
weekday_sales = weekday_sales.sort_values("Weekday")

weekday_sales.to_csv(os.path.join(OUTPUT_DIR, "weekday_sales.csv"), index=False)

# 5.3 Hour-of-day sales
hour_sales = (
    delivered
    .groupby("Hour", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "delivered_sales"})
    .sort_values("Hour")
)
hour_sales.to_csv(os.path.join(OUTPUT_DIR, "hour_sales.csv"), index=False)

# ========= 6. PRODUCT / CATEGORY TABLES =========

# 6.1 Top products by revenue (you can filter in Power BI if needed)
product_sales = (
    delivered
    .groupby("Description", as_index=False)
    .agg(
        delivered_sales=("Sales", "sum"),
        delivered_quantity=("DeliveredQuantity", "sum")
    )
    .sort_values("delivered_sales", ascending=False)
)
product_sales.to_csv(os.path.join(OUTPUT_DIR, "product_sales.csv"), index=False)

# 6.2 Category sales
cat_sales = (
    delivered
    .groupby("Categoty", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "delivered_sales"})
    .sort_values("delivered_sales", ascending=False)
)
# add contribution %
cat_sales["contribution_pct"] = cat_sales["delivered_sales"] / cat_sales["delivered_sales"].sum() * 100
cat_sales.to_csv(os.path.join(OUTPUT_DIR, "category_sales.csv"), index=False)

# 6.3 Sub-category sales
subcat_sales = (
    delivered
    .groupby("Sub_Category", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "delivered_sales"})
    .sort_values("delivered_sales", ascending=False)
)
subcat_sales.to_csv(os.path.join(OUTPUT_DIR, "sub_category_sales.csv"), index=False)

# ========= 7. COUNTRY & CUSTOMER TABLES =========

# 7.1 Country sales
country_sales = (
    delivered
    .groupby("Country", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "delivered_sales"})
    .sort_values("delivered_sales", ascending=False)
)
country_sales.to_csv(os.path.join(OUTPUT_DIR, "country_sales.csv"), index=False)

# 7.2 Customer summary
customer_summary = (
    delivered
    .groupby("CustomerID", as_index=False)
    .agg(
        total_sales=("Sales", "sum"),
        orders=("InvoiceNo", "nunique"),
        total_quantity=("DeliveredQuantity", "sum")
    )
)
customer_summary["avg_order_value"] = customer_summary["total_sales"] / customer_summary["orders"]
customer_summary.to_csv(os.path.join(OUTPUT_DIR, "customer_summary.csv"), index=False)

# ========= 8. RETURNS & CANCELLATIONS / LEAKAGE TABLES =========

# 8.1 Status-level summary
status_sales = (
    df
    .groupby("Status", as_index=False)
    .agg(
        gross_sales=("Gross_Sales", "sum"),
        net_sales=("Sales", "sum"),
        lost_on_cancels=("LostOnCancles", "sum"),
        lost_on_returns=("LostOnReturns", "sum")
    )
)
status_sales["total_lost"] = status_sales["lost_on_cancels"] + status_sales["lost_on_returns"]
status_sales.to_csv(os.path.join(OUTPUT_DIR, "status_sales_summary.csv"), index=False)

# 8.2 Category-level leakage
loss_by_cat = (
    df
    .groupby("Categoty", as_index=False)
    .agg(
        lost_on_cancels=("LostOnCancles", "sum"),
        lost_on_returns=("LostOnReturns", "sum")
    )
)
loss_by_cat["total_loss"] = loss_by_cat["lost_on_cancels"] + loss_by_cat["lost_on_returns"]
loss_by_cat = loss_by_cat.sort_values("total_loss", ascending=False)
loss_by_cat.to_csv(os.path.join(OUTPUT_DIR, "category_leakage.csv"), index=False)

# 8.3 Product-level leakage
loss_by_product = (
    df
    .groupby("Description", as_index=False)
    .agg(
        lost_on_cancels=("LostOnCancles", "sum"),
        lost_on_returns=("LostOnReturns", "sum")
    )
)
loss_by_product["total_loss"] = loss_by_product["lost_on_cancels"] + loss_by_product["lost_on_returns"]
loss_by_product = loss_by_product.sort_values("total_loss", ascending=False)
loss_by_product.to_csv(os.path.join(OUTPUT_DIR, "product_leakage.csv"), index=False)

print(f"✅ All tables exported to folder: {OUTPUT_DIR}")
