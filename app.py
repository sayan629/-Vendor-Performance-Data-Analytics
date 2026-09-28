import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Vendor Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

sales = pd.read_csv("data/sales.csv")
purchases = pd.read_csv("data/purchases.csv")

# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

sales.columns = sales.columns.str.strip()
purchases.columns = purchases.columns.str.strip()

# ============================================================
# BASIC CALCULATIONS
# ============================================================

total_sales = sales["SalesDollars"].sum()
total_purchase = purchases["Dollars"].sum()

gross_profit = total_sales - total_purchase

profit_margin = (
    gross_profit / total_sales * 100
    if total_sales != 0
    else 0
)

# ============================================================
# VENDOR LEVEL DATA
# ============================================================

vendor_sales = (
    sales.groupby("VendorName", as_index=False)
    .agg(
        TotalSales=("SalesDollars", "sum")
    )
)

vendor_purchase = (
    purchases.groupby("VendorName", as_index=False)
    .agg(
        TotalPurchase=("Dollars", "sum")
    )
)

vendor_df = pd.merge(
    vendor_sales,
    vendor_purchase,
    on="VendorName",
    how="left"
)

vendor_df["TotalPurchase"] = vendor_df["TotalPurchase"].fillna(0)

vendor_df["GrossProfit"] = (
    vendor_df["TotalSales"]
    - vendor_df["TotalPurchase"]
)

vendor_df["ProfitMargin"] = (
    vendor_df["GrossProfit"]
    / vendor_df["TotalSales"]
    * 100
)

# Remove invalid values
vendor_df = vendor_df.replace(
    [float("inf"), -float("inf")],
    0
)

vendor_df = vendor_df.dropna(
    subset=["TotalSales", "ProfitMargin"]
)

# ============================================================
# BRAND LEVEL DATA
# ============================================================

brand_sales = (
    sales.groupby("Brand", as_index=False)
    .agg(
        TotalSales=("SalesDollars", "sum")
    )
)

# ============================================================
# TOP / LOW THRESHOLDS
# ============================================================

top_threshold = vendor_df["TotalSales"].quantile(0.75)
low_threshold = vendor_df["TotalSales"].quantile(0.25)

vendor_df["Performance"] = vendor_df["TotalSales"].apply(
    lambda x:
        "Low Performing"
        if x <= low_threshold
        else "Top Performing"
        if x >= top_threshold
        else "Average"
)

# ============================================================
# HEADER
# ============================================================

st.title("Vendor Performance Dashboard")

st.markdown(
    "Analysis of vendor sales, purchases, profitability and performance."
)

st.divider()

# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Sales ($)",
    f"${total_sales / 1_000_000:.2f}M"
)

col2.metric(
    "Total Purchase ($)",
    f"${total_purchase / 1_000_000:.2f}M"
)

col3.metric(
    "Gross Profit ($)",
    f"${gross_profit / 1_000_000:.2f}M"
)

col4.metric(
    "Profit Margin (%)",
    f"{profit_margin:.1f}%"
)

# Unsold capital will be added once we connect inventory data
col5.metric(
    "Unsold Capital ($)",
    "N/A"
)

# ============================================================
# PURCHASE CONTRIBUTION + TOP VENDORS + TOP BRANDS
# ============================================================

col1, col2, col3 = st.columns(3)

# ------------------------------------------------------------
# PURCHASE CONTRIBUTION
# ------------------------------------------------------------

with col1:

    st.subheader("Purchase Contribution %")

    top_purchase_vendors = (
        vendor_df
        .sort_values("TotalPurchase", ascending=False)
        .head(10)
    )

    fig_donut = px.pie(
        top_purchase_vendors,
        values="TotalPurchase",
        names="VendorName",
        hole=0.55
    )

    fig_donut.update_layout(
        height=400,
        showlegend=True,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )

# ------------------------------------------------------------
# TOP VENDORS
# ------------------------------------------------------------

with col2:

    st.subheader("Top Vendors By Sales")

    top_vendors = (
        vendor_df
        .sort_values("TotalSales", ascending=False)
        .head(10)
        .sort_values("TotalSales")
    )

    fig_vendor = px.bar(
        top_vendors,
        x="TotalSales",
        y="VendorName",
        orientation="h",
        text_auto=".2s"
    )

    fig_vendor.update_layout(
        height=400,
        xaxis_title="Sales ($)",
        yaxis_title="",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        fig_vendor,
        use_container_width=True
    )

# ------------------------------------------------------------
# TOP BRANDS
# ------------------------------------------------------------

with col3:

    st.subheader("Top Brands By Sales")

    top_brands = (
        brand_sales
        .sort_values("TotalSales", ascending=False)
        .head(10)
        .sort_values("TotalSales")
    )

    fig_brand = px.bar(
        top_brands,
        x="TotalSales",
        y="Brand",
        orientation="h",
        text_auto=".2s"
    )

    fig_brand.update_layout(
        height=400,
        xaxis_title="Sales ($)",
        yaxis_title="",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        fig_brand,
        use_container_width=True
    )

# ============================================================
# LOW PERFORMING VENDORS
# ============================================================

st.divider()

col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("Low Performing Vendors")

    low_vendors = (
        vendor_df[
            vendor_df["Performance"] == "Low Performing"
        ]
        .sort_values("TotalSales")
        .head(5)
    )

    fig_low = px.bar(
        low_vendors.sort_values("ProfitMargin"),
        x="ProfitMargin",
        y="VendorName",
        orientation="h",
        text="ProfitMargin"
    )

    fig_low.update_traces(
        texttemplate="%{text:.2f}%"
    )

    fig_low.update_layout(
        height=400,
        xaxis_title="Profit Margin (%)",
        yaxis_title="",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        fig_low,
        use_container_width=True
    )

# ============================================================
# SALES VS PROFIT MARGIN
# ============================================================

with col2:

    st.subheader("Vendor Sales vs Profit Margin")

    fig_scatter = px.scatter(
        vendor_df,
        x="TotalSales",
        y="ProfitMargin",
        color="Performance",
        hover_name="VendorName",
        size="TotalSales",
        opacity=0.75
    )

    fig_scatter.update_layout(
        height=400,
        xaxis_title="Total Sales ($)",
        yaxis_title="Profit Margin (%)",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

# ============================================================
# SUMMARY
# ============================================================

st.divider()

st.subheader("Vendor Performance Summary")

st.write(
    f"""
    **Top-performing vendor threshold:** 
    ${top_threshold:,.2f}

    **Low-performing vendor threshold:** 
    ${low_threshold:,.2f}

    **Number of vendors:** 
    {len(vendor_df):,}

    **Top-performing vendors:** 
    {len(vendor_df[vendor_df["Performance"] == "Top Performing"]):,}

    **Low-performing vendors:** 
    {len(vendor_df[vendor_df["Performance"] == "Low Performing"]):,}
    """
)