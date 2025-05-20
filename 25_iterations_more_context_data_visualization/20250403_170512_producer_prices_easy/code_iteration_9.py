# Automatically saved code from agent execution
# Run ID: 20250403_170512_producer_prices_easy, Iteration: 9

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set the style for the plot
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("colorblind")

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/ppi.csv')

# Convert the 'Periods' column to datetime format
def convert_period_to_date(period):
    # Check if the period is just a year
    if str(period).isdigit() or (len(str(period)) == 4 and str(period).isdigit()):
        # For annual data, use July 1st (mid-year)
        return datetime(int(period), 7, 1)
    
    # For monthly data
    parts = str(period).split()
    if len(parts) >= 2:
        year = int(parts[0])
        month_name = parts[1]
        
        # Convert month name to month number
        month_dict = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        month = month_dict.get(month_name, 1)  # Default to 1 if not found
        
        # Create date (using the 1st day of the month)
        return datetime(year, month, 1)
    
    # Default case (should not happen with clean data)
    return None

# Apply the conversion
df['Date'] = df['Periods'].apply(convert_period_to_date)

# Filter out rows with None dates (if any)
df = df.dropna(subset=['Date'])

# Filter to only include monthly data (exclude annual aggregates)
monthly_df = df[df['Periods'].str.contains(' ')]

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

# Define main product categories to analyze
main_categories = ['B Mining and quarrying', 'C Manufacturing', 'D Electricity, gas, steam and air conditioning']

# Plot 1: Compare different product categories (Total sales only)
for category in main_categories:
    category_data = monthly_df[
        (monthly_df['ProductsAccordingToPRODCOMList'] == category) & 
        (monthly_df['OutputAndImportPrices'] == 'Total sales')
    ]
    
    if len(category_data) > 0:
        # Sort by date to ensure proper line plotting
        category_data = category_data.sort_values('Date')
        
        axes[0].plot(
            category_data['Date'], 
            category_data['PriceIndexNumbersExcludingExcise_1'],
            label=category,
            linewidth=2
        )

# Configure the first subplot
axes[0].set_title('Producer Price Index by Product Category (Total Sales, 2015=100)', fontsize=14)
axes[0].set_ylabel('Price Index (2015=100)', fontsize=12)
axes[0].legend(title='Product Category', fontsize=10)
axes[0].grid(True, alpha=0.3)
axes[0].axhline(y=100, color='gray', linestyle='--', alpha=0.7)

# Plot 2: Compare different sales types for Mining and quarrying
sales_types = ['Total sales', 'Domestic sales', 'Foreign sales']
product_category = 'B Mining and quarrying'  # Focus on one product category for clarity

for sales_type in sales_types:
    sales_data = monthly_df[
        (monthly_df['ProductsAccordingToPRODCOMList'] == product_category) & 
        (monthly_df['OutputAndImportPrices'] == sales_type)
    ]
    
    if len(sales_data) > 0:
        # Sort by date to ensure proper line plotting
        sales_data = sales_data.sort_values('Date')
        
        axes[1].plot(
            sales_data['Date'], 
            sales_data['PriceIndexNumbersExcludingExcise_1'],
            label=sales_type,
            linewidth=2
        )

# Configure the second subplot
axes[1].set_title(f'Producer Price Index for {product_category} by Sales Type (2015=100)', fontsize=14)
axes[1].set_xlabel('Year', fontsize=12)
axes[1].set_ylabel('Price Index (2015=100)', fontsize=12)
axes[1].legend(title='Sales Type', fontsize=10)
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=100, color='gray', linestyle='--', alpha=0.7)

# Format the x-axis to show years
for ax in axes:
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax.tick_params(axis='x', rotation=45)

# Add annotations for key events
axes[0].annotate('COVID-19\nPandemic', xy=(datetime(2020, 3, 1), 80), xytext=(datetime(2020, 1, 1), 50),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=10)

axes[0].annotate('Energy Crisis\n2021-2022', xy=(datetime(2022, 1, 1), 350), xytext=(datetime(2021, 6, 1), 300),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=10)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170512_producer_prices_easy/visualization.png', dpi=300)