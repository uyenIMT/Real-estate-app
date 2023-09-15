import streamlit as st
import pandas as pd
from analytics_reports.reports import plot_average_prices
from analytics_reports.reports import plot_by_category

# from property_listings.property_listings import display_property_listings
# from market_trends.market_trends import display_market_trends
# from data_analysis.data_analysis import display_data_analysis

# Load your real estate data into a DataFrame
data = pd.read_csv('data/data.csv')

# Title of your app
st.title('Vietnam Real Estate')

# Sidebar menu
menu = st.sidebar.selectbox('Menu', [
    'Analytics Reports',
    'Property Listings',
    'Market Trends',
    'Data Analysis'
])

# Market Overview page
if menu == 'Analytics Reports':
    st.header('Analytics Reports')
    st.sidebar.header('Select Category')
    selected_category = st.sidebar.selectbox('Choose a Category', data['Category'].unique())
    plot_average_prices(selected_category)
    plot_by_category(selected_category)

# Property Listings page
elif menu == 'Property Listings':
    display_property_listings(data)

# Market Trends page
elif menu == 'Market Trends':
    display_market_trends(data)

# Data Analysis page
elif menu == 'Data Analysis':
    display_data_analysis(data)
