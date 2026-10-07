import streamlit as st
import pandas as pd

st.set_page_config(page_title= 'Home', layout= 'wide')

# --- UNIVERSAL PLATFORM SAFE IMAGE CONTROLLER ---
def display_app_header_safely(filename='images.jpeg'):
    # Check 1: Check absolute root workspace execution path
    if os.path.exists(filename):
        st.image(filename, use_container_width=True)
        return True
    
    # Check 2: Check up one directory levels (if running inside /pages/ folder)
    parent_path = os.path.join('..', filename)
    if os.path.exists(parent_path):
        st.image(parent_path, use_container_width=True)
        return True
        
    # Check 3: Check explicitly relative to project root bounds
    explicit_root_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(explicit_root_path):
        st.image(explicit_root_path, use_container_width=True)
        return True
        
    # Fallback: Gracefully pass text blocks if the graphic is deleted/renamed
    st.info(f"💡 Visual element layout active — Header graphic asset '{filename}' omitted.")
    return False

# Trigger the safe image block configuration
display_app_header_safely('images.jpeg')

html ="""
    <div style="text-align: center; color: #FF4B4B; font-size: 30px; font-weight: bold;">
        Epsilon Amr Ecommerce Mid project
    </div>
    """
st.markdown(html, unsafe_allow_html= True)

# Load Data
df = pd.read_parquet('cleaned_data.parquet')

# Show sample of data
st.subheader('Data Overview')
st.dataframe(df)

import streamlit as st
import pandas as pd
import os

# --- SAFE IMAGE LOOKUP PIPELINE ---
# List all possible places and names your image might have on the cloud server
possible_image_paths = [
    'images.jpeg',                     # Root folder, lowercase extension
    'images.jpg',                      # Root folder, short extension
    'images.png',                      # Root folder, png variant
    os.path.join('pages', 'images.jpeg'),  # Inside pages folder
    os.path.join('pages', 'images.jpg'),   # Inside pages folder variant
    os.path.join('pages', 'images.png')    # Inside pages folder variant
]

image_loaded = False
for path in possible_image_paths:
    if os.path.exists(path):
        st.image(path, use_container_width=True)
        image_loaded = True
        break

# Fallback layout item if the file is completely missing from GitHub
if not image_loaded:
    st.info("💡 Header graphic 'images.jpeg' not found on server—loading text layout.")



