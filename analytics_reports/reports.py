import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter  # Import ScalarFormatter
import plotly.express as px
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

# Extract location
input = 'data/data_test.csv'
output = 'data/data_test_city.csv'
# Load the addresses file into a DataFrame
addresses_df = pd.read_csv(input, encoding='UTF-8-SIG')
# print(addresses_df.head())

# Load the cities/districts file into a DataFrame
cities_districts_df = pd.read_csv('data/Cities.csv', encoding='UTF-8-SIG')

# Function to find city and district for each address
def find_city_district(location):
    location = str(location)  # Ensure location is a string
    for index, row in cities_districts_df.iterrows():
        if str(row["City"]) in location and str(row["District"]) in location:
            return row["City"], row["District"]
    return None, None

# Apply the function to the addresses DataFrame
addresses_df[["City", "District"]] = addresses_df["Location"].apply(find_city_district).apply(pd.Series)

# Save the new DataFrame to a CSV file
addresses_df.to_csv(output, index=False)

data = pd.read_csv('data/data_test_city.csv')
print(data.info())

df = data.dropna(subset = 'Price')
df = df.dropna(subset = 'City')
df=df[~((df['Price'] == 'Thỏa thuận'))]
df['Price'] = pd.to_numeric(df['Price'].str.replace(',', ''), errors='coerce')
df['Price'].astype(float)

print(df.info())

def plot_minmax_prices(selected_category):
    # Filter the data based on the selected category
    filtered_data = df[df['Category'] == selected_category]
    
    # Create a pivot table
    pivot_table = filtered_data.pivot_table(index=['City', 'Category'], values='Price', aggfunc=['min', 'max']).reset_index()
    print(pivot_table.head())
    pivot_table.columns=['City','Category','Min Price','Max Price']
    # Display the data table for the filtered data
    st.subheader('Tổng hợp Giá bất động sản cao nhất và thấp nhất ở các tỉnh thành')
    st.write(pivot_table)

def plot_by_category(selected_category):
    # Get the unique city names and sort them alphabetically
    unique_cities = sorted(df['City'].unique())
    selected_city = st.sidebar.selectbox('Chọn thành phố hoặc tỉnh', unique_cities)
    # Filter the data for the selected city
    filtered_data = df[(df['City'] == selected_city) & (df['Category'] == selected_category)]
    # Display the data table for the filtered data
    # st.write('### Data Table')
    # st.write(filtered_data)

    # Check if data is empty
    if filtered_data.empty:
        print("filtered_data is empty")
        st.write(f"No data available for {selected_category} in {selected_city}.")
    else:
        # Plot Number of property by District
        st.subheader(f'Số lượng bất động sản {selected_category} ở {selected_city}')
        plt.figure(figsize=(10, 15))
        sns.countplot(data=filtered_data, y='District')
        plt.xticks(rotation=25)  # Rotate x-axis labels for better readability
        plt.xlabel('Số lượng')
        plt.ylabel('Quận/Huyện')
        st.pyplot()

        # Plot Price per Area
        st.subheader(f'Giá bất động sản {selected_category} theo M² ở {selected_city}')
        # Create a new column for Price per Area
        filtered_data['Price per Area'] = filtered_data['Price'] / filtered_data['Area']
        # Plot the data
        plt.figure(figsize=(10, 10))
        sns.barplot(data=filtered_data,y='District',x='Price per Area')
        plt.xticks(rotation=45)
        plt.xlabel('Giá trung bình')
        plt.ylabel('Quận/Huyện')
        # Show the full number of price instead of scientific notation
        plt.ticklabel_format(style='plain', axis='x')
        st.pyplot()

        # Plot the estate type by City
        # Create a pie chart showing the proportion of estate types by city
        st.subheader(f'Loại bất động sản ở {selected_city}')
        estate_type_counts = filtered_data['Estate type'].value_counts()
        fig = px.pie(
        values=estate_type_counts.values,
        names=estate_type_counts.index,
        )
        # Display the chart
        st.plotly_chart(fig)

        # Plot the certification status by City
        # Replace empty values (including spaces) with NaN in the 'Certification Status' column
        filtered_data['Certification status'] = filtered_data['Certification status'].replace(' ', pd.NA)
        # Replace blank (empty) values with "Không xác định" in the 'Certification Status' column
        filtered_data['Certification status'].fillna("Không xác định", inplace=True)
        certification_count = len(filtered_data[filtered_data['Certification status'].notna()])
        if certification_count == 0:
            st.write('')
        else:
            # Create a pie chart showing the proportion of certification status by city
            st.subheader(f'Tình trạng pháp lý của bất động sản ở {selected_city}')
            certification_counts = filtered_data['Certification status'].value_counts()
            fig = px.pie(
            values=certification_counts.values,
            names=certification_counts.index,
            )
            # Display the chart
            st.plotly_chart(fig)

        # Plot the directions per city and Category
        direction_count = len(filtered_data[filtered_data['Direction'].notna()])
        if direction_count == 0:
            st.write('')
        else:
            # Create a pie chart showing the proportion of estate types by city
            st.subheader(f'Hướng bất động sản {selected_category} ở {selected_city}')
            # Create a horizontal bar chart
            plt.figure(figsize=(10, 6))
            sns.set(style='whitegrid')
            sns.countplot(data=filtered_data, x="Direction", palette="Spectral")
            plt.xlabel('Hướng')
            plt.ylabel('Số lượng')
            # plt.title(f'Directions of property in {selected_city}')
            plt.show()
            # Display the chart
            st.pyplot()

        # Create a pie chart showing the proportion of estate types by city
        st.subheader(f'Tỷ lệ bất động sản có chỗ đậu xe ở {selected_city}')
        # Create a pie chart to show the proportion of parking slot and non-parking slot
        # parking_slot_count = filtered_data[filtered_data['Parking slot'].notna()]['Parking slot'].count()
        parking_slot_count = len(filtered_data[~np.isnan(filtered_data['Parking slot'])])
        # non_parking_slot_count = filtered_data[filtered_data['Parking slot'].isna()]['Parking slot'].count()
        non_parking_slot_count = len(filtered_data[np.isnan(filtered_data['Parking slot'])])
        fig_pie = px.pie(
        names=['Có chỗ đậu xe', 'Không có chỗ đậu xe'],
        values=[parking_slot_count, non_parking_slot_count]
        )
        # Display the pie chart
        st.plotly_chart(fig_pie)
        if parking_slot_count == 0:
            st.write('')
        else:
            st.subheader(f'Số lượng chỗ đậu xe ở {selected_city}')
            filtered_data2 = filtered_data[filtered_data['Parking slot'].notna() & (filtered_data['Parking slot'] != ' ')]
            # Create a horizontal bar chart
            plt.figure(figsize=(6, 8))
            sns.set(style="whitegrid")
            sns.countplot(data=filtered_data2, x="Parking slot", palette="Spectral")
            plt.xlabel('Số lượng chỗ đậu xe/bất động sản')
            plt.ylabel('Số lượng')
            # Display the chart
            st.pyplot()
    
        # Create a pie chart showing the proportion of estate types by city
        st.subheader(f'Tỷ lệ người bán ở {selected_city}')
        # Create a pie chart to show the proportion of parking slot and non-parking slot
        personal_count = filtered_data[filtered_data['Seller type'] == 'Cá Nhân - Chính Chủ']['Seller type'].count()
        non_personal_count = filtered_data[filtered_data['Seller type'] == 'Công Ty Nhà Đất - Môi Giới BĐS']['Seller type'].count()
        fig_pie = px.pie(
        names=['Cá Nhân - Chính Chủ', 'Công Ty Nhà Đất - Môi Giới BĐS'],
        values=[personal_count, non_personal_count],
        )
        # Display the pie chart
        st.plotly_chart(fig_pie)
        
   
