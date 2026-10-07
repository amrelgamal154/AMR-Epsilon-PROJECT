import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Home', layout='wide')

try:
    st.image('photorealistic-scene-with-warehouse-logistics-operations_23-2151468808.jpg.avif')
except:
    st.warning("⚠️ 'images.jpeg' not found. Please verify the file path.")

html = """
    <div style="text-align: center; color: #FF4B4B; font-size: 30px; font-weight: bold;">
        Logistics review for Depot construction
    </div>
    """
st.markdown(html, unsafe_allow_html=True)

# 1. Load Data
@st.cache_data
def get_data():
    return pd.read_parquet('cleaned_data.parquet')

df = get_data()

# 2. Filter US Data ('Estados Unidos')
if 'Order Country' in df.columns:
    df_us = df[df['Order Country'] == 'Estados Unidos']
else:
    df_us = df

# Show sample of data


st.write("### US Data Filtered")
st.dataframe(df_us.head(50), use_container_width=True)


# --- 3. Compute Your Clusters ---
northeast_cities = ['New York City', 'Philadelphia', 'Newark', 'Richmond']
western_cities = ['Los Angeles', 'San Francisco', 'San Diego']

northeast_total = df_us[df_us['Order City'].isin(northeast_cities)]['Sales'].sum()
western_total = df_us[df_us['Order City'].isin(western_cities)]['Sales'].sum()


# --- 4. Build the KPI Interface Layout ---
st.subheader("📦 Regional Cluster Comparison")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🗽 Northeast Cluster Sales", 
        value=f"${northeast_total:,.2f}"
    )

with col2:
    st.metric(
        label="🌴 Western Cluster Sales", 
        value=f"${western_total:,.2f}"
    )

with col3:
    sales_diff = northeast_total - western_total
    pct_diff = (sales_diff / western_total) * 100 if western_total != 0 else 0
    
    st.metric(
        label="Variance (Northeast vs Western)",
        value=f"${sales_diff:,.2f}",
        delta=f"{pct_diff:+.2f}% vs Western",
        delta_color="normal" if sales_diff >= 0 else "inverse"
    )


# --- 5. Layout Breakdown: Chart Analysis (Left) vs Illustrative Info (Right Side) ---
st.markdown("---")
st.subheader("📊 Cluster Analytics & Regional Directories")

main_visuals, illustrative_side = st.columns([2, 1]) # 2:1 ratio keeping info tightly on the side

with main_visuals:
    # A. Sales Distribution Plot
    st.write("#### Sales Distribution Chart")
    cluster_summary = pd.DataFrame({
        'Cluster': ['Northeast Cluster', 'Western Cluster'],
        'Total Sales': [northeast_total, western_total]
    })
    fig_sales = px.bar(
        cluster_summary, 
        x='Cluster', 
        y='Total Sales', 
        color='Cluster',
        text_auto='.3s',
        color_discrete_sequence=['#4B6584', '#F7B731']
    )
    fig_sales.update_layout(height=300, margin=dict(t=20, b=20))
    st.plotly_chart(fig_sales, use_container_width=True)
    
    st.markdown("---")
    
    # B. Logistics Late Delivery Risk Plot
    st.write("#### Top Cities by Late Delivery Risk")
    if 'Late_delivery_risk' in df_us.columns and 'Order City' in df_us.columns:
        risk_df = df_us.groupby('Order City')['Late_delivery_risk'].sum().reset_index()
        risk_df = risk_df.sort_values(by='Late_delivery_risk', ascending=False)
    else:
        risk_data = {
            'Order City': [
                'New York City', 'Los Angeles', 'Philadelphia', 'San Francisco', 'Seattle', 
                'Houston', 'Chicago', 'Columbus', 'San Diego', 'Springfield', 'Dallas'
            ],
            'Late_delivery_risk': [2202, 1845, 1302, 1297, 1066, 875, 789, 550, 425, 379, 374]
        }
        risk_df = pd.DataFrame(risk_data)

    fig_risk = px.bar(
        risk_df.head(10), 
        x='Late_delivery_risk', 
        y='Order City', 
        orientation='h',
        text_auto=True,
        color='Late_delivery_risk',
        color_continuous_scale='Reds',
        labels={'Late_delivery_risk': 'Risk Count', 'Order City': 'City'}
    )
    fig_risk.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, height=320, margin=dict(t=20, b=20))
    st.plotly_chart(fig_risk, use_container_width=True)

with illustrative_side:
    # Sidebar Text Reference Card
    st.markdown("### 📋 Node Blueprint")
    with st.container(border=True):
        st.markdown(
            "#### 🗽 Northeast Cluster\n"
            "* **New York City** — Primary Core Hub\n"
            "* **Philadelphia** — Regional Fulfillment\n"
            "* **Newark** — Inbound Port Gateway\n"
            "* **Richmond** — Mid-Atlantic Node\n\n"
            "--- \n\n"
            "#### 🌴 Western Cluster\n"
            "* **Los Angeles** — Primary Pacific Gateway\n"
            "* **San Francisco** — Northern CA Transit\n"
            "* **San Diego** — Cross-Border Hub"
        )
        
    # Calculated Risk Summary Totals under the blueprint card
    ne_risk = risk_df[risk_df['Order City'].isin(northeast_cities)]['Late_delivery_risk'].sum()
    w_risk = risk_df[risk_df['Order City'].isin(western_cities)]['Late_delivery_risk'].sum()
    higher_risk_cluster = "Northeast" if ne_risk > w_risk else "Western"
    
    st.write("#### 🚨 Quick Risk Audit")
    st.metric(label="Northeast Incidents", value=f"{ne_risk:,}")
    st.metric(label="Western Incidents", value=f"{w_risk:,}")
    st.error(f"The **{higher_risk_cluster} Cluster** contains the largest overall concentration of transit delivery delay risks.")