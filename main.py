import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading the Dataset
data = pd.read_csv('https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv')

# Convert date column to datetime type
data['date'] = pd.to_datetime(data['date'])

# Data Inspection
# Checking the range of dates
date_range = data['date'].min(), data['date'].max()
print(f"Date Range: {date_range}")

# Understanding the distribution of sales
sales_distribution = data['sale_dollars'].describe()
print("\nSales Distribution:\n", sales_distribution)

# Filtering the data to include only the years 2016 to 2019
data = data[(data['date'].dt.year >= 2016) & (data['date'].dt.year <= 2019)]

# Handling missing values in analyzing columns
# Dropping rows where crucial columns have missing values
important_columns = ['zip_code', 'item_description', 'sale_dollars', 'store_number']
data.dropna(subset=important_columns, inplace=True)

# Checking the cleaned dataset
print("\nCleaned Dataset Info:")
data.info()
print(data.head())






# Assuming 'bottles_sold' and 'item_number' are columns in your DataFrame and you want to sum bottles_sold per zip_code
bottles_per_zipcode = data.groupby(['zip_code', 'item_number'])['bottles_sold'].sum().reset_index()

# Sorting the values to get the top items
top_items = bottles_per_zipcode.sort_values('bottles_sold', ascending=False).head(5)

# Create the scatter plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as necessary
scatter = plt.scatter(bottles_per_zipcode['zip_code'], bottles_per_zipcode['bottles_sold'], c=bottles_per_zipcode['bottles_sold'], cmap='tab20b')

# Annotate only the top 5 items by bottles sold
for _, row in top_items.iterrows():
    zip_codes_for_item = data[data['item_number'] == row['item_number']]['zip_code'].tolist()
    for zip_code in zip_codes_for_item:
        bottles_sold_for_zip = data[(data['zip_code'] == zip_code) & (data['item_number'] == row['item_number'])]['bottles_sold'].sum()
        plt.annotate(row['item_number'],  # Text to annotate
                     (zip_code, bottles_sold_for_zip),  # Point to annotate
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center',  # horizontal alignment can be left, right, or center
                     fontsize=9,  # font size of annotation
                     color='black')  # text color

# Add labels and title
plt.xlabel('Zipcode')
plt.ylabel('Bottles sold')
plt.title('Sales Visualization')

# Show color bar
plt.colorbar(scatter, label='Bottles sold')

# Show the plot
plt.show()



# Assuming you have already loaded and processed the dataset as shown in your provided code

# Filter the data for the timeframe 2016-2019
filtered_data = data[(data['date'].dt.year >= 2016) & (data['date'].dt.year <= 2019)]

# Calculate the total sales per store for the filtered data
total_sales_per_store = filtered_data.groupby('store_number')['sale_dollars'].sum().reset_index(name='total_sales')

# Calculate the sales percentage
overall_total_sales = total_sales_per_store['total_sales'].sum()
total_sales_per_store['sales_percentage'] = (total_sales_per_store['total_sales'] / overall_total_sales) * 100

# Merge with store_name from the original dataset to get store names
total_sales_per_store = total_sales_per_store.merge(data[['store_number', 'store_name']].drop_duplicates(), on='store_number', how='left')

# Sort the DataFrame by sales_percentage in ascending order
total_sales_per_store = total_sales_per_store.sort_values('sales_percentage', ascending=True)

# Select the top 15 stores
top_15_stores = total_sales_per_store.tail(15)

# Create a Seaborn barplot to visualize the sales percentage per store
plt.figure(figsize=(12, 6))
ax = sns.barplot(x='sales_percentage', y='store_name', data=top_15_stores, palette='Paired')
plt.xlabel('% Sales')
plt.ylabel('Store Name')
plt.title('Top 15 Stores by Sales Percentage (2016-2019)')
plt.grid(axis='x', linestyle='--', alpha=0.6)  # Add grid lines for better visualization

# Annotate the bars with the sales percentages
for p in ax.patches:
    width = p.get_width()
    plt.annotate(f'{width:.2f}%', (width, p.get_y() + p.get_height() / 2), ha='center')

# Show the plot
plt.tight_layout()
plt.show()





