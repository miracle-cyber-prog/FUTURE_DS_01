import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Business Sales Dashboard", layout="wide")

# ---------------------------
# STYLE
# ---------------------------
st.markdown("""
<style>

.stApp{
    background-color: black;
    color: white;
}

.metric-box{
    background-color:#111111;
    padding:15px;
    border-radius:0px;
    text-align:center;
    border:2px solid white;
}

.metric-title{
    color:#aaaaaa;
    font-size:14px;
}

.metric-value{
    font-size:26px;
    font-weight:bold;
    color:#00FFFF;
}


</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("datasets/sales.csv")

# ---------------------------
# SIDEBAR
# ---------------------------

st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

state_filter = st.sidebar.multiselect(
    "State",
    df["State"].unique(),
    default=df["State"].unique()
)

year_filter = st.sidebar.multiselect(
    "Year",
    df["Year"].unique(),
    default=df["Year"].unique()
)

filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["State"].isin(state_filter)) &
    (df["Year"].isin(year_filter))
]

# ---------------------------
# KPI METRICS
# ---------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
customer_count = filtered_df["Customer Name"].nunique()
avg_profit = filtered_df["Profit"].mean()

st.title("Business Sales Analytics Dashboard")

k1,k2,k3,k4 = st.columns(4)

k1.markdown(f'<div class="metric-box"><div class="metric-title">Total Sales</div><div class="metric-value">${total_sales:,.0f}</div></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="metric-box"><div class="metric-title">Total Profit</div><div class="metric-value">${total_profit:,.0f}</div></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="metric-box"><div class="metric-title">Customer Count</div><div class="metric-value">{customer_count}</div></div>', unsafe_allow_html=True)
k4.markdown(f'<div class="metric-box"><div class="metric-title">Avg Profit</div><div class="metric-value">${avg_profit:,.0f}</div></div>', unsafe_allow_html=True)

# ---------------------------
# DATA PREPARATION
# ---------------------------
sales_month = filtered_df.groupby("Month")["Sales"].sum().reset_index()
sales_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()
sales_state = filtered_df.groupby("State")["Sales"].sum().reset_index()
top_customers = filtered_df.groupby("Customer Name")["Profit"].sum().reset_index().sort_values(by="Profit", ascending=False).head(5)
profit_year = filtered_df.groupby("Year")["Profit"].sum().reset_index()

customer_distribution = filtered_df["Customer Name"].value_counts().reset_index()
customer_distribution.columns = ["Customer Name","Count"]
customer_distribution = customer_distribution.head(5)

# ---------------------------
# CHART ROW 1
# ---------------------------
c1,c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig1 = px.line(
        sales_month,
        x="Month",
        y="Sales",
        title="Sales by Month",
        markers=True,
        color_discrete_sequence=["cyan"]
    )

    fig1.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white"
    )

    st.plotly_chart(fig1,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig2 = px.bar(
        top_customers,
        x="Customer Name",
        y="Profit",
        title="Top 5 Customers by Profit",
        color="Profit",
        color_continuous_scale=["cyan","purple"]
    )

    fig2.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white"
    )

    st.plotly_chart(fig2,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# CHART ROW 2
# ---------------------------
c3,c4 = st.columns(2)

with c3:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig3 = px.bar(
        sales_category,
        x="Category",
        y="Sales",
        title="Sales by Category",
        color="Category"
    )

    fig3.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white"
    )

    st.plotly_chart(fig3,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig4 = px.bar(
        sales_state,
        x="State",
        y="Sales",
        title="Sales by State",
        color="Sales",
        color_continuous_scale=["cyan","purple"]
    )

    fig4.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white"
    )

    st.plotly_chart(fig4,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# CHART ROW 3
# ---------------------------
c5,c6 = st.columns(2)

with c5:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig5 = px.bar(
        profit_year,
        x="Year",
        y="Profit",
        title="Profit by Year",
        color="Profit",
        color_continuous_scale=["cyan","purple"]
    )

    fig5.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white"
    )

    st.plotly_chart(fig5,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with c6:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig6 = px.pie(
        customer_distribution,
        values="Count",
        names="Customer Name",
        title="Customer Distribution"
    )

    fig6.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white"
    )

    st.plotly_chart(fig6,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
### Insights
◽ Identify revenue-driving categories
            
◽ track seasonal sales trends
            
◽ Discover high value customers
            
◽ Understad regional performance               
""")