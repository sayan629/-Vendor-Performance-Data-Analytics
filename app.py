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
# THEME / COLOR PALETTE  (UI only)
# ============================================================

PRIMARY = "#4F46E5"     # indigo
SECONDARY = "#14B8A6"   # teal
ACCENT = "#F59E0B"      # amber
DANGER = "#F43F5E"      # rose
INK = "#1E293B"
MUTED = "#64748B"
GRID = "#E2E8F0"

PIE_COLORS = [
    "#4F46E5", "#14B8A6", "#F59E0B", "#F43F5E", "#8B5CF6",
    "#0EA5E9", "#22C55E", "#EC4899", "#F97316", "#64748B"
]

PERFORMANCE_COLORS = {
    "Top Performing": SECONDARY,
    "Average": PRIMARY,
    "Low Performing": DANGER
}


def style_fig(fig):
    """Apply a consistent look to every plotly chart."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color=INK,
            size=13
        ),
        legend=dict(
            title_text="",
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=INK)
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        )
    )
    fig.update_xaxes(
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
        automargin=True,
        title_standoff=12
    )
    fig.update_yaxes(
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
        automargin=True,
        title_standoff=12
    )
    # room for labels/titles + outside bar text
    fig.update_layout(
        margin=dict(l=20, r=60, t=30, b=30)
    )
    fig.update_traces(
        cliponaxis=False,
        selector=dict(type="bar")
    )
    return fig


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: linear-gradient(180deg, #F5F7FB 0%, #EEF2F9 100%);
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    /* Title */
    h1 {{
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 0;
    }}

    [data-testid="stCaptionContainer"] {{
        color: {MUTED};
        font-size: 1rem;
    }}

    /* Force readable text regardless of Streamlit light/dark theme */
    .stApp, .stApp p, .stApp span, .stApp label {{
        color: {INK};
    }}

    /* Section headings */
    h3, h3 span, h3 div, h3 a {{
        color: {INK} !important;
    }}

    [data-testid="stHeading"] h3 {{
        font-weight: 600 !important;
        border-left: 5px solid {PRIMARY};
        padding-left: 12px;
        margin-bottom: 0.5rem;
    }}

    /* Dividers */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #CBD5E1, transparent);
        margin: 1.5rem 0;
    }}

    /* KPI cards */
    [data-testid="stMetric"] {{
        background: #FFFFFF;
        border-radius: 16px;
        padding: 18px 22px;
        box-shadow: 0 4px 14px rgba(30, 41, 59, 0.07);
        border-top: 4px solid {PRIMARY};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    [data-testid="stMetric"]:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 24px rgba(79, 70, 229, 0.18);
    }}

    [data-testid="column"]:nth-child(2) [data-testid="stMetric"] {{
        border-top-color: {SECONDARY};
    }}
    [data-testid="column"]:nth-child(3) [data-testid="stMetric"] {{
        border-top-color: {ACCENT};
    }}
    [data-testid="column"]:nth-child(4) [data-testid="stMetric"] {{
        border-top-color: #8B5CF6;
    }}
    [data-testid="column"]:nth-child(5) [data-testid="stMetric"] {{
        border-top-color: {DANGER};
    }}

    [data-testid="stMetricLabel"] p {{
        color: {MUTED} !important;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }}

    [data-testid="stMetricValue"], [data-testid="stMetricValue"] div {{
        color: {INK} !important;
        font-weight: 700;
    }}

    /* Chart cards */
    [data-testid="stPlotlyChart"] {{
        background: #FFFFFF;
        border-radius: 16px;
        padding: 0;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(30, 41, 59, 0.07);
    }}
    </style>
    """,
    unsafe_allow_html=True
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

    fig_vendor.update_traces(
        marker_color=PRIMARY,
        marker_line_width=0,
        textposition="outside",
        cliponaxis=False
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
        style_fig(fig_vendor),
        use_container_width=True,
        theme=None
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

    fig_brand.update_traces(
        marker_color=SECONDARY,
        marker_line_width=0,
        textposition="outside",
        cliponaxis=False
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

    fig_brand.update_yaxes(type="category")

    st.plotly_chart(
        style_fig(fig_brand),
        use_container_width=True,
        theme=None
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
    hole=0.55,
    color_discrete_sequence=PIE_COLORS
)

fig_purchase.update_traces(
    marker=dict(line=dict(color="white", width=2))
)

fig_purchase.update_layout(
    height=450
)

st.plotly_chart(
    style_fig(fig_purchase),
    use_container_width=True,
    theme=None
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
        texttemplate="%{text:.2f}%",
        marker_color=DANGER,
        marker_line_width=0
    )

    fig_low_vendor.update_layout(
        height=450,
        xaxis_title="Profit Margin (%)",
        yaxis_title=""
    )

    st.plotly_chart(
        style_fig(fig_low_vendor),
        use_container_width=True,
        theme=None
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
        texttemplate="%{text:.2f}%",
        marker_color=ACCENT,
        marker_line_width=0
    )

    fig_low_brand.update_layout(
        height=450,
        xaxis_title="Profit Margin (%)",
        yaxis_title=""
    )

    fig_low_brand.update_yaxes(type="category")

    st.plotly_chart(
        style_fig(fig_low_brand),
        use_container_width=True,
        theme=None
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
    opacity=0.75,
    color_discrete_map=PERFORMANCE_COLORS
)

fig_scatter.update_traces(
    marker=dict(line=dict(color="white", width=0.5))
)

fig_scatter.update_layout(
    height=550,
    xaxis_title="Total Sales ($)",
    yaxis_title="Profit Margin (%)"
)

st.plotly_chart(
    style_fig(fig_scatter),
    use_container_width=True,
    theme=None
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