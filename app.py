import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("Ecommerce_dataset_updated.csv")

df["order_date"] = pd.to_datetime(df["order_date"])

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("E-Commerce Sales & Business Analytics Dashboard")
st.markdown("Interactive analysis of sales, profit, customers, and orders.")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

years = sorted(df["order_year"].dropna().unique())

selected_year = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

categories = sorted(df["category"].dropna().unique())

selected_category = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

countries = sorted(df["country"].dropna().unique())

selected_country = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=countries
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df[
    (df["order_year"].isin(selected_year)) &
    (df["category"].isin(selected_category)) &
    (df["country"].isin(selected_country))
]

# -----------------------------
# KPI Calculations
# -----------------------------
total_revenue = filtered_df["total_price_usd"].sum()

total_orders = filtered_df["order_id"].nunique()

total_profit = filtered_df["profit_usd"].sum()

if total_orders > 0:
    average_order_value = total_revenue / total_orders
else:
    average_order_value = 0

if total_revenue > 0:
    profit_margin = (total_profit / total_revenue) * 100
else:
    profit_margin = 0

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "🛒 Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "💵 Average Order Value",
    f"${average_order_value:,.2f}"
)

col4.metric(
    "📈 Total Profit",
    f"${total_profit:,.2f}"
)

col5.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

# -----------------------------
# Monthly Sales Trend
# -----------------------------
monthly_sales = (
    filtered_df
    .groupby(filtered_df["order_date"].dt.to_period("M"))
    .agg(
        Revenue=("total_price_usd", "sum"),
        Profit=("profit_usd", "sum")
    )
    .reset_index()
)

monthly_sales["order_date"] = (
    monthly_sales["order_date"].astype(str)
)

fig_sales = px.line(
    monthly_sales,
    x="order_date",
    y="Revenue",
    markers=True,
    title="📈 Monthly Revenue Trend"
)

fig_sales.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (USD)"
)

st.plotly_chart(
    fig_sales,
    use_container_width=True
)

# -----------------------------
# Category Analysis
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    category_sales = (
        filtered_df
        .groupby("category")["total_price_usd"]
        .sum()
        .reset_index()
        .sort_values("total_price_usd", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="category",
        y="total_price_usd",
        title="💰 Sales by Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with col2:

    category_profit = (
        filtered_df
        .groupby("category")["profit_usd"]
        .sum()
        .reset_index()
        .sort_values("profit_usd", ascending=False)
    )

    fig_profit = px.bar(
        category_profit,
        x="category",
        y="profit_usd",
        title="📈 Profit by Category"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

# -----------------------------
# Country Analysis
# -----------------------------
country_sales = (
    filtered_df
    .groupby("country")["total_price_usd"]
    .sum()
    .reset_index()
    .sort_values("total_price_usd", ascending=False)
    .head(10)
)

fig_country = px.bar(
    country_sales,
    x="total_price_usd",
    y="country",
    orientation="h",
    title="🌍 Top 10 Countries by Revenue"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

# -----------------------------
# Payment Method Analysis
# -----------------------------
payment_sales = (
    filtered_df
    .groupby("payment_method")["total_price_usd"]
    .sum()
    .reset_index()
)

fig_payment = px.pie(
    payment_sales,
    names="payment_method",
    values="total_price_usd",
    title="💳 Revenue by Payment Method"
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "E-Commerce Sales & Business Analytics Dashboard | "
    "EncoderX Remote Internship Batch 02"
)