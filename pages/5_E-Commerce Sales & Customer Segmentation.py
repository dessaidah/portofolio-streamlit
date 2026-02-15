import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

st.set_page_config(layout="wide", page_title="E-Commerce Analytics")

st.markdown("""
<style>

body {
    background-color: #F5F7FA;
}

.main {
    background-color: #F5F7FA;
}

h1 {
    font-weight: 600;
    color: #1F3C88;
}

h2, h3 {
    color: #1F3C88;
    font-weight: 600;
}

.metric-card {
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #6B7280;
}

.metric-value {
    font-size: 28px;
    font-weight: 600;
    color: #1F3C88;
}

.section-divider {
    margin-top: 40px;
    margin-bottom: 40px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent  
    # parent.parent karena file ada di folder pages

    sales_path = BASE_DIR / "projects" / "models" / "base_sales.csv"
    rfm_path   = BASE_DIR / "projects" / "models" / "rfm_table.csv"

    sales = pd.read_csv(sales_path, parse_dates=["created_at"])
    rfm   = pd.read_csv(rfm_path)

    return sales, rfm

sales, rfm = load_data()
sales["created_at"] = pd.to_datetime(sales["created_at"], errors="coerce")
st.write(sales["created_at"].dtype)
# ======================
# FILTER LAST 1 YEAR
# ======================
max_date = sales["created_at"].max()
one_year_ago = max_date - pd.DateOffset(years=1)
sales_1y = sales[sales["created_at"] >= one_year_ago]

# ======================
# TITLE
# ======================
st.title("E-Commerce Sales & Customer Segmentation")

st.markdown(
"<p style='color:#6B7280;'>Premium Sales Performance & RFM Intelligence Dashboard</p>",
unsafe_allow_html=True
)

# ======================
# KPI SECTION
# ======================
total_revenue = sales_1y["sale_price"].sum()
total_orders = sales_1y["order_id"].nunique()
avg_order_value = total_revenue / total_orders
avg_margin = sales_1y["margin_pct"].mean()

col1, col2, col3, col4 = st.columns(4)

def metric_card(title, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

with col1:
    metric_card("Revenue (Last 1 Year)", f"${total_revenue:,.0f}")

with col2:
    metric_card("Total Orders", f"{total_orders:,}")

with col3:
    metric_card("Avg Order Value", f"${avg_order_value:,.1f}")

with col4:
    metric_card("Avg Margin", f"{avg_margin:.1%}")

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ======================
# REVENUE TREND
# ======================
sales_1y["order_month"] = sales_1y["created_at"].dt.to_period("M").astype(str)

monthly = sales_1y.groupby("order_month")["sale_price"].sum().reset_index()

fig_trend = px.line(monthly, x="order_month", y="sale_price")

fig_trend.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=10, t=30, b=10),
    font=dict(color="#374151"),
)

fig_trend.update_traces(line=dict(color="#1F3C88", width=3))

st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ======================
# RFM DISTRIBUTION
# ======================
st.subheader("Customer Segmentation (RFM)")

rfm_dist = rfm["rfm_segment"].value_counts().reset_index()
rfm_dist.columns = ["Segment", "Customers"]

fig_pie = px.pie(
    rfm_dist,
    names="Segment",
    values="Customers",
    hole=0.65
)

fig_pie.update_layout(
    showlegend=True,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ======================
# REVENUE BY SEGMENT
# ======================
merged = sales_1y.merge(
    rfm[["user_id", "rfm_segment"]],
    on="user_id",
    how="left"
)

segment_rev = (
    merged.groupby("rfm_segment")["sale_price"]
    .sum()
    .reset_index()
    .sort_values("sale_price", ascending=False)
)

fig_bar = px.bar(
    segment_rev,
    x="sale_price",
    y="rfm_segment",
    orientation="h"
)

fig_bar.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

fig_bar.update_traces(marker_color="#1F3C88")

st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ======================
# RETENTION IMPACT SIMULATOR
# ======================
st.subheader("Retention Impact Simulation")

hib_rev = segment_rev.loc[
    segment_rev["rfm_segment"] == "Hibernating",
    "sale_price"
]

hib_rev = hib_rev.values[0] if len(hib_rev) > 0 else 0

reactivation = st.slider("Reactivation Rate (%)", 0, 30, 10)
repeat_uplift = st.slider("Repeat Purchase Increase (%)", 0, 20, 10)

reactivation_gain = hib_rev * (reactivation / 100)
repeat_gain = total_revenue * (repeat_uplift / 100)
total_gain = reactivation_gain + repeat_gain

col1, col2, col3 = st.columns(3)

with col1:
    metric_card("Reactivation Potential", f"${reactivation_gain:,.0f}")

with col2:
    metric_card("Repeat Purchase Uplift", f"${repeat_gain:,.0f}")

with col3:
    metric_card("Total Revenue Impact", f"${total_gain:,.0f}")

st.markdown(
"""
<p style='color:#6B7280;'>
Improving retention even marginally can unlock significant incremental revenue 
without increasing acquisition cost.
</p>
""",
unsafe_allow_html=True
)

st.caption("Premium Minimalist Dashboard • Streamlit")
