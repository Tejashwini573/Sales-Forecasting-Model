
# 1. IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 2. LOAD DATASET
df = pd.read_csv("ecommerce_sales_data (2).csv")

print("First 5 Rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

# 3. DATA CLEANING

# Remove duplicates
df.drop_duplicates(inplace=True)

# Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Handle missing values
df.fillna(df.median(numeric_only=True), inplace=True)
df.fillna(df.mode().iloc[0], inplace=True)

# 4. DATE PROCESSING (if Order_Date exists)

if "Order_Date" in df.columns:
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Day"] = df["Order_Date"].dt.day


# 5. CREATE TOTAL REVENUE COLUMN (if needed)

if "Quantity" in df.columns and "Price" in df.columns:
    df["Total_Revenue"] = df["Quantity"] * df["Price"]

# If Sales column already exists, use that
if "Sales" in df.columns:
    df["Total_Revenue"] = df["Sales"]

# 6. BASIC KPI CALCULATIONS

total_revenue = df["Total_Revenue"].sum()
total_orders = len(df)

print("\nTotal Revenue:", total_revenue)
print("Total Orders:", total_orders)

if "Profit" in df.columns:
    total_profit = df["Profit"].sum()
    print("Total Profit:", total_profit)

# 7. EXPLORATORY DATA ANALYSIS (EDA)

# 7.1 Monthly Sales Trend
if "Month" in df.columns:
    monthly_sales = df.groupby("Month")["Total_Revenue"].sum()

    plt.figure()
    monthly_sales.plot()
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue")
    plt.show()

# 7.2 Top 10 Products
if "Product" in df.columns:
    top_products = df.groupby("Product")["Total_Revenue"].sum().sort_values(ascending=False).head(10)

    plt.figure()
    top_products.plot(kind="bar")
    plt.title("Top 10 Products by Revenue")
    plt.show()

# 7.3 Sales by Category
if "Category" in df.columns:
    category_sales = df.groupby("Category")["Total_Revenue"].sum()

    plt.figure()
    category_sales.plot(kind="bar")
    plt.title("Revenue by Category")
    plt.show()

# 7.4 Sales by Region
if "Region" in df.columns:
    region_sales = df.groupby("Region")["Total_Revenue"].sum()

    plt.figure()
    region_sales.plot(kind="bar")
    plt.title("Revenue by Region")
    plt.show()

# 7.5 Profit by Category
if "Profit" in df.columns and "Category" in df.columns:
    profit_analysis = df.groupby("Category")["Profit"].sum()

    plt.figure()
    profit_analysis.plot(kind="bar")
    plt.title("Profit by Category")
    plt.show()

# 7.6 Correlation Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.title("Correlation Heatmap")
plt.show()

# 8. SAVE CLEANED DATA

df.to_csv("cleaned_ecommerce_sales_data.csv", index=False)
print("\nProject Completed Successfully ✅")