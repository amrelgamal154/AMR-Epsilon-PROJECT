import streamlit as st
import pandas as pd
import os

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(page_title='Home - Epsilon Ecommerce', layout='wide', page_icon='🛒')

# --- 2. FAIL-SAFE IMAGE BANNER LOADING ---
image_filename = 'images.jpeg'
image_found = False

if os.path.exists(image_filename):
    st.image(image_filename, use_container_width=True)
    image_found = True
elif os.path.exists(os.path.join('pages', image_filename)):
    st.image(os.path.join('pages', image_filename), use_container_width=True)
    image_found = True
elif os.path.exists(os.path.join(os.getcwd(), image_filename)):
    st.image(os.path.join(os.getcwd(), image_filename), use_container_width=True)
    image_found = True

if not image_found:
    st.info("💡 Graphic header asset 'images.jpeg' omitted from preview layout.")

# --- 3. TITLE BLOCK ---
html_title = """
    <div style="text-align: center; color: #FF4B4B; font-size: 34px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;">
        🛒 Epsilon Amr Ecommerce Mid Project
    </div>
    <div style="text-align: center; color: #666666; font-size: 16px; margin-bottom: 25px;">
        Interactive Portfolio Data Discovery Hub
    </div>
    """
st.markdown(html_title, unsafe_allow_html=True)

# --- 4. DYNAMIC PARQUET FILE EXTRACTION ---
data_filename = 'cleaned_data.parquet'
df = pd.DataFrame()

if os.path.exists(data_filename):
    df = pd.read_parquet(data_filename)
elif os.path.exists(os.path.join(os.getcwd(), data_filename)):
    df = pd.read_parquet(os.path.join(os.getcwd(), data_filename))
elif os.path.exists(os.path.join('..', data_filename)):
    df = pd.read_parquet(os.path.join('..', data_filename))

# --- 5. INTERACTIVE SUMMARY METRICS ---
st.markdown("### 📊 Initial Dataset Profile")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(label="📐 Initial Footprint Attributes", value="53 Columns", delta="Raw Structural Dimension")
with kpi2:
    total_rows = f"{len(df):,}" if not df.empty else "Parsing..."
    st.metric(label="📋 Total Registered Records", value=total_rows, delta="Active Data Rows")
with kpi3:
    market_focus = "United States Focus" if not df.empty else "Pending"
    st.metric(label="🎯 Optimized Regional Focus", value=market_focus, delta="Estados Unidos Share")

st.markdown("---")

# --- 6. DATA RENDER PLATFORM ---
if not df.empty:
    st.subheader('📦 Data Overview Snippet')
    st.dataframe(df.head(15), use_container_width=True, hide_index=True)
else:
    st.error(f"📂 Operational File Error: '{data_filename}' could not be located in workspace paths.")
    st.info("💡 Troubleshooting check: Ensure the dataset file is uploaded directly to the main root folder of your repository on GitHub.")

st.markdown("---")

# --- 7. EXPLORATION PERSPECTIVES DIRECTORY (INTERACTIVE) ---
st.subheader("💡 Analytical Scopes & Project Perspectives")
st.write("Click on each perspective below to preview the core objectives explored in this data portfolio:")

# 3-Column structural layout for clean scannability
p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    with st.expander("🚚 Logistics & Infrastructure", expanded=False):
        st.markdown(
            "#### **Depot Allocation Strategy**\n"
            "* **Objective:** Identify transit network constraints across regional hub densities.\n"
            "* **Metric Focus:** Mapping total delay indices (`Late_delivery_risk`) against location models.\n"
            "* **Outcome:** Targeted physical fulfillment infrastructure investment layout for **New York City** and **Los Angeles** hubs."
        )

with p_col2:
    with st.expander("📉 Commercial Sales Trajectory", expanded=False):
        st.markdown(
            "#### **Revenue Trend Line Analysis**\n"
            "* **Objective:** Evaluate multi-year gross merchant metrics and trace transaction behavior patterns.\n"
            "* **Feature Engineering:** Aggregating transaction logs using chronological `data order_date formatted` steps.\n"
            "* **Outcome:** Identified and flagged a severe final reported fiscal year volume drop to trigger a sales team data audit workflow."
        )

with p_col3:
    with st.expander("🖥️ Streamlit App Architecture", expanded=False):
        st.markdown(
            "#### **User-Friendly Analytics Tool**\n"
            "* **Objective:** Transition rigid programming scripts into reactive executive decision dashboards.\n"
            "* **Interactive Assets:** Multi-select components restricted to active `Order City` strings and real-time range sliders.\n"
            "* **Performance Engine:** Incorporates `@st.cache_data` parameter loading layers to process file arrays instantly without runtime friction."
        )
