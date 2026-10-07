# Epsilon Amr Ecommerce Mid Project

A Streamlit-based business intelligence project focused on exploring ecommerce and supply-chain performance using a cleaned retail dataset. The app presents a landing page and multiple analytical views that highlight sales performance, regional logistics behavior, and delivery-risk patterns across the United States.

## Project Overview

This project was designed as an interactive analytics portfolio to support data discovery and executive-style reporting. It combines structured data preparation with dashboard-style visualizations to answer practical business questions such as:

- Which cities and categories drive the most sales?
- How do logistics clusters compare in revenue generation and delay risk?
- What are the major sales trends over time?
- Which operational bottlenecks deserve attention in the network?

## Key Features

- Interactive landing page with dataset summary and analytical scope overview
- KPI cards for sales, customer count, and regional data profile
- Multi-page Streamlit dashboard structure
- US-focused product, city, and category analysis
- Regional logistics comparisons for Northeast vs. Western clusters
- Late-delivery risk review for major cities
- Historical sales trend analysis across 2015-2018
- Plotly-based charts for trending and comparison visuals

## Project Structure

```text
AMR Epsilon PROJECT/
├── homepage.py                  # Main landing page for the app
├── streamlit.py                 # Additional Streamlit entry script
├── DataCoSupplyChainDataset.csv # Source dataset
├── cleaned_data.parquet         # Cleaned data used by the dashboard
├── images.jpeg                  # Banner image asset
├── requirements.txt             # Python dependencies
├── amr_project.ipynb            # Notebook exploration work
├── streamlit.ipynb              # Streamlit notebook prototype
├── pages/
│   ├── Dashboard.py             # US sales + category dashboard
│   ├── Logistics_report.py      # Regional logistics and risk analysis
│   └── Sales_trend_report.py    # Historical sales trend report
└── README.md                    # Project documentation
```

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Parquet data handling

## Installation

1. Clone or download the project folder.
2. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

From the project root, start the dashboard with:

```bash
streamlit run homepage.py
```

If the project is configured for multi-page navigation, the pages will appear automatically in the Streamlit sidebar when the app is launched.

## Data Notes

- The app expects the cleaned dataset file `cleaned_data.parquet` to be present in the project root.
- If the parquet file is missing, the dashboard may show a file-location warning.
- The raw dataset `DataCoSupplyChainDataset.csv` is included for source/reference purposes and can be used for additional preprocessing or exploratory analysis.

## Business Use Case

The dashboard is intended to support data-driven decision-making in ecommerce and logistics operations by combining sales insights with operational risk views. It is especially useful for understanding:

- revenue concentration by geography and category
- market demand patterns
- logistics bottlenecks and risk-prone regions
- year-over-year performance shifts

## Authoring Context

This project is part of the AMR Epsilon data science coursework and serves as a mid-project portfolio dashboard for supply-chain and ecommerce analytics.

## License

This project does not include a formal license file. If you plan to reuse or distribute it, confirm the intended licensing requirements before publishing externally.
