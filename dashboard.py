import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('Dashboard_Dataset_After.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Total_Amount'] = pd.to_numeric(df['Total_Amount'], errors='coerce').fillna(0)
    df['Product_Category'] = df['Product_Category'].astype(str).str.strip()
    df['Status'] = df['Status'].astype(str).str.strip()
    return df

df = load_data()

st.sidebar.header("🔍 Control Panel")
selected_cats = st.sidebar.multiselect("Product Categories", sorted(df['Product_Category'].unique()), default=df['Product_Category'].unique())
selected_status = st.sidebar.multiselect("Order Status", sorted(df['Status'].unique()), default=df['Status'].unique())

mask = (df['Product_Category'].isin(selected_cats)) & (df['Status'].isin(selected_status))
df_filtered = df[mask].copy()

st.title("📊 Sales Analytics Intelligence")

total_rev = df_filtered['Total_Amount'].sum()
revenue_display = f"${total_rev/1e6:.1f}M" if total_rev >= 1e6 else f"${total_rev:,.0f}"

avg_val = df_filtered['Total_Amount'].mean()
avg_display = f"${avg_val/1e3:.1f}K" if avg_val >= 1e3 else f"${avg_val:,.2f}"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", revenue_display)
c2.metric("Total Orders", f"{len(df_filtered):,}")
c3.metric("Avg Order Value", avg_display)
c4.metric("Filtered Records", f"{len(df_filtered):,}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Revenue Trend (Millions)")
    trend = df_filtered.groupby(df_filtered['Date'].dt.to_period('M'))['Total_Amount'].sum().reset_index()
    trend['Date'] = trend['Date'].dt.to_timestamp()
    trend['Millions'] = trend['Total_Amount'] / 1e6
    st.line_chart(trend.set_index('Date')['Millions'], color="#00CC96", height=400)

with col2:
    st.subheader("💰 Revenue by Category (Millions)")
    cat_summary = df_filtered.groupby("Product_Category")["Total_Amount"].sum().reset_index()
    cat_summary['Millions'] = (cat_summary['Total_Amount'] / 1e6).round(1)
    
    cat_chart = alt.Chart(cat_summary).mark_bar().encode(
        x=alt.X('Product_Category:N', axis=alt.Axis(labelAngle=-45)),
        y='Millions:Q',
        color='Product_Category:N',
        tooltip=['Product_Category', 'Millions']
    ).properties(height=400)
    st.altair_chart(cat_chart, use_container_width=True)

st.markdown("---")

b_col1, b_col2 = st.columns([1, 2])

with b_col1:
    st.subheader("📦 Order Fulfillment")
    status_summary = df_filtered.groupby("Status")["Total_Amount"].sum().reset_index()
    total_val = status_summary["Total_Amount"].sum()
    status_summary['Millions'] = (status_summary['Total_Amount'] / 1e6).round(1)
    status_summary['Percent'] = (status_summary['Total_Amount'] / total_val * 100).round(1).astype(str) + '%'

    base = alt.Chart(status_summary).encode(
        theta=alt.Theta("Total_Amount:Q", stack=True),
        color=alt.Color("Status:N", legend=alt.Legend(title="Order Status")),
        tooltip=["Status", "Millions", "Percent"]
    )

    pie = base.mark_arc(outerRadius=120, innerRadius=60)
    
    text = base.mark_text(radius=145, size=14, fontWeight="bold").encode(
        text="Percent:N"
    )

    st.altair_chart((pie + text).properties(width=400, height=450), use_container_width=True)

with b_col2:
    st.subheader("🏆 Top 10 High-Value Customers (Millions)")
    top_cust_df = df_filtered.groupby("Customer_Name")["Total_Amount"].sum().nlargest(10).reset_index()
    top_cust_df['Millions'] = (top_cust_df['Total_Amount'] / 1e6).round(1)
    
    cust_chart = alt.Chart(top_cust_df).mark_bar().encode(
        x=alt.X('Customer_Name:N', sort='-y', axis=alt.Axis(labelAngle=-45)),
        y='Millions:Q',
        color='Customer_Name:N',
        tooltip=['Customer_Name', 'Millions']
    ).properties(height=500)
    st.altair_chart(cust_chart, use_container_width=True)