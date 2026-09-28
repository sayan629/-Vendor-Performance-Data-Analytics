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
# LOAD PROCESSED DATA
# ============================================================

vendor_df = pd.read_csv(
    "data/dashboard_vendor_summary.csv"
)

brand_df = pd.read_csv(
    "data/dashboard_brand_summary.csv"
)


# ============================================================
# BASIC CLEANING
# ============================================================

vendor_df["TotalSales"] = pd.to_numeric(
    vendor_df["TotalSales"],
    errors="coerce"
).fillna(0)

vendor_df["TotalPurchase"] = pd.to_numeric(
    vendor_df["TotalPurchase"],
    errors="coerce"
).fillna(0)

vendor_df["GrossProfit"] = pd.to_numeric(
    vendor_df["GrossProfit"],
    errors="coerce"
).fillna(0)

vendor_df["ProfitMargin"] = pd.to_numeric(
    vendor_df["ProfitMargin"],
    errors="coerce"
).fillna(0)

brand_df["TotalSales"] = pd.to_numeric(
    brand_df["TotalSales"],
    errors="coerce"
).fillna(0)

brand_df["TotalPurchase"] = pd.to_numeric(
    brand_df["TotalPurchase"],
    errors="coerce"
).fillna(0)

brand_df["GrossProfit"] = pd.to_numeric(
    brand_df["GrossProfit"],
    errors="coerce"
).fillna(0)

brand_df["ProfitMargin"] = pd.to_numeric(
    brand_df["ProfitMargin"],
    errors="coerce"
).fillna(0)


# ============================================================
# OVERALL KPIs
# ============================================================

total_sales = vendor_df["TotalSales"].sum()

total_purchase = vendor_df["TotalPurchase"].sum()

gross_profit = (
    total_sales - total_purchase
)

profit_margin = (
    gross_profit / total_sales * 100
    if total_sales != 0
    else 0
)


# ============================================================
# VENDOR PERFORMANCE CLASSIFICATION
# ============================================================

top_threshold = vendor_df["TotalSales"].quantile(0.75)

low_threshold = vendor_df["TotalSales"].quantile(0.25)


vendor_df["Performance"] = vendor_df[
    "TotalSales"
].apply(
    lambda x:
        "Low Performing"
        if x <= low_threshold
        else
        "Top Performing"
        if x >= top_threshold
        else
        "Average"
)


# ============================================================
# HEADER
# ============================================================

st.title("Vendor Performance Dashboard")

st.caption(
    "Vendor sales, purchasing and profitability analysis"
)

st.divider()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        "Total Sales",
        f"${total_sales / 1_000_000:.2f}M"
    )


with col2:
    st.metric(
        "Total Purchase",
        f"${total_purchase / 1_000_000:.2f}M"
    )


with col3:
    st.metric(
        "Gross Profit",
        f"${gross_profit / 1_000_000:.2f}M"
    )


with col4:
    st.metric(
        "Profit Margin",
        f"{profit_margin:.1f}%"
    )


with col5:
    st.metric(
        "Total Vendors",
        f"{len(vendor_df):,}"
    )


st.divider()


# ============================================================
# TOP VENDORS / TOP BRANDS
# ============================================================

top_vendors = (
    vendor_df
    .nlargest(10, "TotalSales")
    .sort_values("TotalSales")
)

top_brands = (
    brand_df
    .nlargest(10, "TotalSales")
    .sort_values("TotalSales")
)


col1, col2 = st.columns(2)


# ============================================================
# TOP VENDORS
# ============================================================

with col1:

    st.subheader("Top Vendors By Sales")

    fig_vendor = px.bar(
        top_vendors,
        x="TotalSales",
        y="VendorName",
        orientation="h",
        text_auto=".2s"
    )

    fig_vendor.update_layout(
        height=450,
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


# ============================================================
# TOP BRANDS
# ============================================================

with col2:

    st.subheader("Top Brands By Sales")

    fig_brand = px.bar(
        top_brands,
        x="TotalSales",
        y="Brand",
        orientation="h",
        text_auto=".2s"
    )

    fig_brand.update_layout(
        height=450,
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


st.divider()


# ============================================================
# PURCHASE CONTRIBUTION
# ============================================================

st.subheader("Purchase Contribution")

purchase_top = (
    vendor_df
    .nlargest(10, "TotalPurchase")
)

fig_purchase = px.pie(
    purchase_top,
    values="TotalPurchase",
    names="VendorName",
    hole=0.55
)

fig_purchase.update_layout(
    height=450
)

st.plotly_chart(
    fig_purchase,
    use_container_width=True
)


st.divider()


# ============================================================
# LOW PERFORMING VENDORS
# ============================================================

low_vendors = (
    vendor_df[
        vendor_df["Performance"] == "Low Performing"
    ]
    .nsmallest(10, "TotalSales")
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("Low Performing Vendors")

    fig_low_vendor = px.bar(
        low_vendors.sort_values("ProfitMargin"),
        x="ProfitMargin",
        y="VendorName",
        orientation="h",
        text="ProfitMargin"
    )

    fig_low_vendor.update_traces(
        texttemplate="%{text:.2f}%"
    )

    fig_low_vendor.update_layout(
        height=450,
        xaxis_title="Profit Margin (%)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_low_vendor,
        use_container_width=True
    )


# ============================================================
# LOW PERFORMING BRANDS
# ============================================================

low_brands = (
    brand_df
    .nsmallest(10, "TotalSales")
)


with col2:

    st.subheader("Low Performing Brands")

    fig_low_brand = px.bar(
        low_brands.sort_values("ProfitMargin"),
        x="ProfitMargin",
        y="Brand",
        orientation="h",
        text="ProfitMargin"
    )

    fig_low_brand.update_traces(
        texttemplate="%{text:.2f}%"
    )

    fig_low_brand.update_layout(
        height=450,
        xaxis_title="Profit Margin (%)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_low_brand,
        use_container_width=True
    )


st.divider()


# ============================================================
# SALES VS PROFIT MARGIN
# ============================================================

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
    height=550,
    xaxis_title="Total Sales ($)",
    yaxis_title="Profit Margin (%)"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


st.divider()


# ============================================================
# PERFORMANCE SUMMARY
# ============================================================

st.subheader("Performance Summary")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Top 25% Sales Threshold",
        f"${top_threshold:,.0f}"
    )


with col2:

    st.metric(
        "Bottom 25% Sales Threshold",
        f"${low_threshold:,.0f}"
    )


with col3:

    st.metric(
        "Low Performing Vendors",
        f"{len(low_vendors):,}"
    )