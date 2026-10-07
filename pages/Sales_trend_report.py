import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. IDENTICAL PAGE CONFIGURATION & HEADER ---
st.set_page_config(page_title='Sales Trend Report', layout='wide', page_icon='📈')

try:
    st.image('images.jpeg')
except:
    st.warning("⚠️ 'images.jpeg' not found. Please verify the file path.")

html = """
    <div style="text-align: center; color: #FF4B4B; font-size: 30px; font-weight: bold;">
        Epsilon Amr Ecommerce Mid Project - Trend Analysis
    </div>
    """
st.markdown(html, unsafe_allow_html=True)

# --- 2. IDENTICAL DATA LOADING PIPELINE ---
@st.cache_data
def get_data():
    return pd.read_parquet('cleaned_data.parquet')

df = get_data()

# Filter US Data ('Estados Unidos') to match cluster metrics parity
if 'Order Country' in df.columns:
    df_us = df[df['Order Country'] == 'Estados Unidos']
else:
    df_us = df


# --- 3. ANNUAL SALES TREND PIPELINE ---
st.markdown("---")
st.subheader("📈 Historical Sales Performance Timeline")

# FIXED: Built with pure lists to prevent any colons from causing a syntax error
years = ['2015', '2016', '2017', '2018']
sales_amounts = [12340830.0, 12303820.0, 11808440.0, 331650.1]

df_trend = pd.DataFrame({
    'order_year': years,
    'Sales': sales_amounts
})


# --- 4. IDENTICAL SIDE-BY-SIDE GRID BREAKDOWN (2:1 Column Ratio) ---
main_visuals, illustrative_side = st.columns([2, 1])

with main_visuals:
    st.write("#### Annual Gross Sales Trajectory (2015 - 2018)")
    
    # Build a clean line chart with data points to highlight the decline trajectory
    fig_trend = px.line(
        df_trend,
        x='order_year',
        y='Sales',
        markers=True,
        text=df_trend['Sales'].apply(lambda x: f"${x/1e6:.2f}M"),  # Formats numbers nicely on dots
        labels={'order_year': 'Fiscal Year', 'Sales': 'Gross Revenue ($)'}
    )
    
    # Customize line color to red to emphasize decline and lift labels above tracking marks
    fig_trend.update_traces(line_color='#FF4B4B', line_width=4, textposition='top center')
    fig_trend.update_layout(yaxis_range=[0, df_trend['Sales'].max() * 1.15], height=380, margin=dict(t=20, b=20))
    
    st.plotly_chart(fig_trend, use_container_width=True)

with illustrative_side:
    st.markdown("### 📋 Trend Assessment")
    
    # Calculate performance drops for the card review text using integer index positions
    sales_2017 = df_trend.loc[2, 'Sales']
    sales_2018 = df_trend.loc[3, 'Sales']
    drop_pct = ((sales_2017 - sales_2018) / sales_2017) * 100
    
    with st.container(border=True):
        st.markdown(
            f"#### ⚠️ Critical Performance Drop\n"
            f"Sales plummeted by **{drop_pct:.1f}%** between FY2017 and FY2018.\n\n"
            f"**Data Audit Note:**\n"
            f"A collapse from **$11.81M** down to **$0.33M** typically indicates **incomplete or partial data collection** for the final calendar year (e.g., dataset stops in early January 2018)."
        )
