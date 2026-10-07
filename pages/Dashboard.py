import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE SETUP & THEME INITIALIZATION ---
st.set_page_config(page_title="US Sales & Category Report", layout="wide", page_icon="🇺🇸")

html_title = """
    <div style="text-align: center; color: #FF4B4B; font-size: 32px; font-weight: bold; margin-bottom: 20px;">
        🇺🇸 United States Logistics & Sales Analysis
    </div>
    """
st.markdown(html_title, unsafe_allow_html=True)


# --- 2. EXTRACT, FILTER, AND DATETIME PIPELINE ---
@st.cache_data
def load_clean_us_data():
    try:
        df = pd.read_parquet('cleaned_data.parquet')
    except FileNotFoundError:
        st.error("📂 Could not locate 'cleaned_data.parquet'. Please check file placement.")
        st.stop()

    # Apply your exact country filter first while full dataset is active
    df_filtered = df[df['Order Country'] == 'Estados Unidos'].copy()
    if df_filtered.empty:
        df_filtered = df.copy()  # Safe fallback if country matching variations skip rows

    # EXACT 10 COLUMNS REQUESTED
    requested_columns = [
        'Customer Id', 
        'Customer Lname', 
        'Customer Fname', 
        'Category Name', 
        'Sales', 
        'Order City', 
        'data order_date formatted',  # Fixed to search for exact column string name
        'Product Price', 
        'Order Item Discount Rate'
    ]

    # Flexible matching to find variations like 'data order_date formatted' or 'order_date_formatted'
    matched_columns = []
    actual_col_mapping = {}
    
    for target in requested_columns:
        clean_target = target.lower().replace('_', '').replace(' ', '')
        for actual_col in df_filtered.columns:
            clean_actual = actual_col.lower().replace('_', '').replace(' ', '')
            if clean_actual == clean_target and actual_col not in matched_columns:
                matched_columns.append(actual_col)
                actual_col_mapping[target] = actual_col
                break

    # Extract matching names cleanly
    sales_field = actual_col_mapping.get('Sales', 'Sales')
    city_field = actual_col_mapping.get('Order City', 'Order City')
    date_field = actual_col_mapping.get('data order_date formatted', None)

    # If the exact text string search skipped the target date column, look for partial fallback matching
    if not date_field:
        for actual_col in df_filtered.columns:
            if 'date' in actual_col.lower() and 'format' in actual_col.lower():
                date_field = actual_col
                actual_col_mapping['data order_date formatted'] = actual_col
                if actual_col not in matched_columns:
                    matched_columns.append(actual_col)
                break

    # Build final clean dataframe slice containing exactly the target columns
    final_cols = [c for c in matched_columns if c in df_filtered.columns]
    df_sliced = df_filtered[final_cols].copy()
    
    # --- CONVERT DATE AND PARSE ENTIRE THREE YEARS ---
    if date_field and date_field in df_sliced.columns:
        df_sliced[date_field] = pd.to_datetime(df_sliced[date_field], errors='coerce')
        # Drop missing date fields to prevent slider timeline errors
        df_sliced = df_sliced.dropna(subset=[date_field])
    
    return df_sliced, actual_col_mapping

# Run data pipeline
df_us, mapped_cols = load_clean_us_data()

# Establish clear column names for operations
sales_field = mapped_cols.get('Sales', 'Sales')
city_field = mapped_cols.get('Order City', 'Order City')
cat_field = mapped_cols.get('Category Name', 'Category Name')
date_field = mapped_cols.get('data order_date formatted', 'data order_date formatted')
cust_id_field = mapped_cols.get('Customer Id', 'Customer Id')
discount_field = mapped_cols.get('Order Item Discount Rate', 'Order Item Discount Rate')


# --- 3. DYNAMIC INTERACTIVE FILTER SIDEBAR ---
st.sidebar.header("🕹️ Dashboard Controls & Filters")

# A. SLIDER TO CONTROL THE PIE CHART TOP SLICES
top_n = st.sidebar.slider(
    label="Number of Top Cities/Categories to display:",
    min_value=3, max_value=20, value=10, step=1
)

st.sidebar.markdown("---")

# B. DYNAMIC SIDEBAR MULTISELECT RESTRICED ONLY TO THE "ORDER CITY" COLUMN
if city_field in df_us.columns:
    # Pulls unique entries exclusively from your specific Order City column
    all_cities = sorted(df_us[city_field].dropna().unique())
    selected_cities = st.sidebar.multiselect(
        label="🏙️ Filter by Order City:",
        options=all_cities,
        default=[]  # Left empty by default so it shows all cities unless filtered explicitly
    )
else:
    selected_cities = []

st.sidebar.markdown("---")

# C. DATE RANGE SLIDER CAPTURING ALL THREE HISTORICAL YEARS
if date_field in df_us.columns and not df_us.empty:
    min_date = df_us[date_field].min().date()
    max_date = df_us[date_field].max().date()
    
    if min_date < max_date:
        start_date, end_date = st.sidebar.slider(
            label="📅 Filter by Order Date Range:",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )
    else:
        start_date, end_date = min_date, max_date
else:
    start_date, end_date = None, None


# --- 4. APPLY LIVE SIDEBAR FILTERS ---
df_processed = df_us.copy()

# Filter by selected cities
if selected_cities:
    df_processed = df_processed[df_processed[city_field].isin(selected_cities)]

# Filter by selected date handles
if start_date and end_date and date_field in df_processed.columns:
    df_processed = df_processed[
        (df_processed[date_field].dt.date >= start_date) & 
        (df_processed[date_field].dt.date <= end_date)
    ]


# --- 5. CLEAN DATA SNAPSHOT PREVIEW ---
st.subheader("📋 Sliced 10-Column Data Matrix Snapshot")
if not df_processed.empty:
    df_preview = df_processed.copy()
    if date_field in df_preview.columns:
        df_preview[date_field] = df_preview[date_field].dt.strftime('%Y-%m-%d')
    st.dataframe(df_preview.head(10), use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ No data matches your active filter selection. Try adjusting the date slider variables.")


# --- 6. HIGH-IMPACT METRIC CARDS (KPIs) ---
st.markdown("---")
st.subheader("📌 Key Performance Indicators (US)")

total_sales = df_processed[sales_field].sum() if sales_field in df_processed.columns else 0.0
unique_customers = df_processed[cust_id_field].nunique() if cust_id_field in df_processed.columns else 0

if discount_field in df_processed.columns:
    avg_discount = df_processed[discount_field].mean()
    disp_discount = avg_discount * 100 if avg_discount <= 1.0 else avg_discount
else:
    disp_discount = 0.0

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="💰 Total Gross US Revenue", value=f"${total_sales:,.2f}")
with kpi2:
    st.metric(label="👥 Unique Customers Served", value=f"{unique_customers:,}")
with kpi3:
    st.metric(label="🏷️ Average Discount Rate Applied", value=f"{disp_discount:.2f}%")


# --- 7. VISUAL ANALYTICS INTERFACE (DYNAMIC DONUT PIE CHARTS) ---
st.markdown("---")
chart_col1, chart_col2 = st.columns(2, gap="large")

with chart_col1:
    st.write(f"#### 🏙️ Top {top_n} Cities Distribution by Sales Value")
    if city_field in df_processed.columns and sales_field in df_processed.columns and not df_processed.empty:
        city_sales = df_processed.groupby(city_field)[sales_field].sum().nlargest(top_n).reset_index()
        
        fig_city = px.pie(
            city_sales, values=sales_field, names=city_field, hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_city.update_traces(textposition='inside', textinfo='percent+label')
        fig_city.update_layout(height=420, showlegend=False, margin=dict(t=15, b=15, l=15, r=15))
        st.plotly_chart(fig_city, use_container_width=True)
    else:
        st.info("Adjust the sidebar date handles to view city distribution metrics.")

with chart_col2:
    st.write(f"#### 📦 Top {top_n} Product Categories Generating Sales")
    if cat_field in df_processed.columns and sales_field in df_processed.columns and not df_processed.empty:
        cat_sales = df_processed.groupby(cat_field)[sales_field].sum().nlargest(top_n).reset_index()
        
        fig_cat = px.pie(
            cat_sales, values=sales_field, names=cat_field, hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_cat.update_traces(textposition='inside', textinfo='percent+label')
        fig_cat.update_layout(height=420, showlegend=False, margin=dict(t=15, b=15, l=15, r=15))
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info("Adjust the sidebar date handles to view category distribution metrics.")
