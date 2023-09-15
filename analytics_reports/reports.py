import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter  # Import ScalarFormatter
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

data = pd.read_csv('data/data.csv')
data['Price'] = data['Price'].str.replace(',', '').astype(float)
df = data.dropna(subset = 'Price')
df = df.dropna(subset = 'City')
print(df['Price'].head())

def plot_average_prices(selected_category):
    # Group the data
    grouped_data = df.groupby(['City', 'Category'])['Price'].max().reset_index()

    # Filter the data based on the selected category
    filtered_data = grouped_data[grouped_data['Category'] == selected_category]
    
    # Create a pivot table for plotting
    pivot_data = filtered_data.pivot_table(index='City', columns='Category', values='Price', aggfunc='max')
    
    # Plot the data
    st.subheader(f'Max price by City for {selected_category}')
    plt.figure(figsize=(10, 10))
    sns.barplot(data=pivot_data, y=pivot_data.index, x=selected_category)
    plt.xlabel('Max price')
    plt.ylabel('City')
    st.pyplot()

def plot_by_category(selected_category):
    selected_city = st.sidebar.selectbox('Choose a City', data['City'].unique())
    # Filter the data for the selected city
    filtered_data = data[(data['City'] == selected_city) & (data['Category'] == selected_category)]
     # Display the data table for the filtered data
    st.write('### Data Table')
    st.write(filtered_data)

    # Plot the Price by City
    st.subheader(f'Distribution of Price for {selected_category} in {selected_city}')
    ax= sns.violinplot(x=filtered_data["Price"], bw=.15)
    ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    st.pyplot()

    # Plot Number of property by District
    st.subheader(f'Count of Properties for {selected_category} in {selected_city}')
    plt.figure(figsize=(18, 12))
    sns.countplot(data=filtered_data, x='District')
    plt.xticks(rotation=25)  # Rotate x-axis labels for better readability
    plt.xlabel('District')
    plt.ylabel('Count of Properties')
    st.pyplot()

    # Plot Price per Area
    st.subheader(f'Price of Properties for {selected_category} in {selected_city} per M²')
    # Check if filtered_data is empty
    if filtered_data.empty:
        st.write(f"No data available for {selected_category} in {selected_city}.")
    else:
        # Extract numeric values from the 'Area' column using regular expressions
        filtered_data['Area'] = filtered_data['Area'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    # Create a new column for Price per Area
    filtered_data['Price per Area'] = filtered_data['Price'] / filtered_data['Area']
    # Plot the data
    plt.figure(figsize=(10, 10))
    sns.barplot(data=filtered_data,y='District',x='Price per Area')
    plt.xticks(rotation=45)
    plt.xlabel('Average Price')
    plt.ylabel('District')
    # Format the x-axis tick labels to display the full price without scientific notation
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:g}'))
    st.pyplot()

    # Plot the estate type by City
    # Check if filtered_data is empty
    if filtered_data.empty:
        st.write(f"No data available for {selected_city}.")
    else:
        # Create a pie chart showing the proportion of estate types by city
        st.subheader(f'Estate Type Proportion in {selected_city}')
        estate_type_counts = filtered_data['Estate type'].value_counts()
        # Create a horizontal bar chart
        plt.figure(figsize=(10, 6))
        plt.barh(estate_type_counts.index, estate_type_counts.values)
        plt.xlabel('Proportion '+ f'(%)')
        plt.ylabel('Estate Type')
        plt.title(f'Estate Type Proportion in {selected_city}')
        plt.gca().invert_yaxis()  # Reverse the order of categories for readability
        plt.show()
         # Display the chart
        st.pyplot()





