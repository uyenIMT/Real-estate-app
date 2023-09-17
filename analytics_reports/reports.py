import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter  # Import ScalarFormatter
import plotly.express as px

st.set_option('deprecation.showPyplotGlobalUse', False)

data = pd.read_csv('data/data.csv')
data['Price'] = data['Price'].str.replace(',', '').astype(float)
# data['Parking slot'] = data['Parking slot'].str.replace('(Chỗ)', '')
df = data.dropna(subset = 'Price')
df = df.dropna(subset = 'City')
df=df[~((df['Category'] == 'Sale') & (df['Price'] > 1000000000000))]
df=df[~((df['Category'] == 'Sale') & (df['Price'] < 700000000))]
df=df[~((df['Category'] == 'Rent') & (df['Price'] > 500000000))]
# print(df['Parking slot'].head())

def plot_minmax_prices(selected_category):
    # Filter the data based on the selected category
    filtered_data = df[df['Category'] == selected_category]
    # Create a pivot table
    pivot_table = filtered_data.pivot_table(index=['City', 'Category'], values='Price', aggfunc=['min', 'max']).reset_index()
    pivot_table.columns=['City','Category','Min Price','Max Price']
    # Display the data table for the filtered data
    st.write('### Data Table')
    st.write(pivot_table)
    # Set the figure size
    plt.figure(figsize=(15, 20))
    # Create a bar chart using seaborn
    sns.set(style="whitegrid")
    sns.barplot(data=pivot_table, x='Max Price', y='City', color='lightblue', label='Max Price')
    sns.barplot(data=pivot_table, x='Min Price', y='City', color='lightcoral', label='Min Price')
    plt.xlabel('Price')
    plt.ylabel('City')
    plt.title(f'Min and Max Prices for {selected_category} Category')
    plt.legend()
    # Show the full number of price instead of scientific notation
    plt.ticklabel_format(style='plain', axis='x')
    plt.xticks(rotation=45)
    # Add a title
    plt.title('Max and Min Prices per City and Category')
    # Show the chart
    st.pyplot()

def plot_by_category(selected_category):
    selected_city = st.sidebar.selectbox('Choose a City', data['City'].unique())
    # Filter the data for the selected city
    filtered_data = data[(data['City'] == selected_city) & (data['Category'] == selected_category)]
    # Display the data table for the filtered data
    # st.write('### Data Table')
    # st.write(filtered_data)

    # Plot the Price by City
    st.subheader(f'Distribution of Price for {selected_category} in {selected_city}')
    ax= sns.violinplot(x=filtered_data["Price"], bw=.15)
    ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    # Show the full number of price instead of scientific notation
    plt.ticklabel_format(style='plain', axis='x')
    st.pyplot()

    # Plot Number of property by District
    st.subheader(f'Count of Properties for {selected_category} in {selected_city}')
    plt.figure(figsize=(18, 25))
    sns.countplot(data=filtered_data, y='District')
    plt.xticks(rotation=25)  # Rotate x-axis labels for better readability
    plt.xlabel('Count of Properties')
    plt.ylabel('District')
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
    # Show the full number of price instead of scientific notation
    plt.ticklabel_format(style='plain', axis='x')
    st.pyplot()

    # Plot the estate type by City
    # Check if filtered_data is empty
    if filtered_data.empty:
        st.write(f"No data available for {selected_city}.")
    else:
        # Create a pie chart showing the proportion of estate types by city
        st.subheader(f'Estate Type Proportion in {selected_city}')
        estate_type_counts = filtered_data['Estate type'].value_counts()
        fig = px.pie(
        values=estate_type_counts.values,
        names=estate_type_counts.index,
        title=f'Estate Type Proportion in {selected_city}'
        )
        # Display the chart
        st.plotly_chart(fig)

    # Plot the directions per city and Category
    # Check if filtered_data is empty
    if filtered_data.empty:
        st.write(f"No data available for {selected_city}.")
    else:
        # Create a pie chart showing the proportion of estate types by city
        st.subheader(f'Directions of property in {selected_city}')
        # Create a horizontal bar chart
        plt.figure(figsize=(10, 6))
        sns.set(style='whitegrid')
        sns.countplot(data=filtered_data, x="Direction", palette="Spectral")
        plt.xlabel('Direction')
        plt.ylabel('Count')
        plt.title(f'Directions of property in {selected_city}')
        plt.show()
        # Display the chart
        st.pyplot()

    # Plot the parking slot proportion and number of them
    if filtered_data.empty:
        st.write(f"No data available for {selected_city}.")
    else:
        # Create a pie chart showing the proportion of estate types by city
        st.subheader(f'Parking slot of property in {selected_city}')
        # Create a pie chart to show the proportion of parking slot and non-parking slot
        parking_slot_count = filtered_data[filtered_data['Parking slot'] != ' ']['Parking slot'].count()
        non_parking_slot_count = filtered_data[filtered_data['Parking slot'] == ' ']['Parking slot'].count()
        fig_pie = px.pie(
        names=['Parking Slot', 'No Parking Slot'],
        values=[parking_slot_count, non_parking_slot_count],
        title="Parking Slot Proportion"
        )
        # Display the pie chart
        st.plotly_chart(fig_pie)
        
        st.subheader(f'Count of parking slot of property in {selected_city}')
        filtered_data2 = filtered_data[filtered_data['Parking slot'].notna() & (filtered_data['Parking slot'] != ' ')]
        # Create a horizontal bar chart
        plt.figure(figsize=(6, 8))
        sns.set(style="whitegrid")
        sns.countplot(data=filtered_data2, x="Parking slot", palette="Spectral")
        plt.xlabel('Parking slot')
        plt.ylabel('Count')
        plt.title(f'Count of parking slot of property in {selected_city}')
        plt.show()
        # Display the chart
        st.pyplot()
        
        

