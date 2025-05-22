# Automatically saved code from agent execution
# Run ID: 20250403_170512_producer_prices_easy, Iteration: 11

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

# Check for the main categories in the data
main_categories = ['B Mining and quarrying', 'C Manufacturing', 'D Electricity, gas, steam and air conditioning']
for category in main_categories:
    data = monthly_df[(monthly_df['ProductsAccordingToPRODCOMList'] == category) & 
                      (monthly_df['OutputAndImportPrices'] == 'Total sales')]
    print(f"Category: {category}, Data points: {len(data)}")

# Let's check for other high-level categories that might be available
high_level_categories = monthly_df[monthly_df['ProductsAccordingToPRODCOMList'].str.match(r'^[A-Z]')]
print("\nHigh-level categories:")
print(high_level_categories['ProductsAccordingToPRODCOMList'].unique())

# Let's create a visualization with the available data
# Create a figure with a single plot
plt.figure(figsize=(14, 8))

# Find all high-level categories (starting with a letter)
high_level_cats = [cat for cat in monthly_df['ProductsAccordingToPRODCOMList'].unique() 
                  if isinstance(cat, str) and cat[0].isalpha() and cat[1] == ' ']

# Plot each high-level category
for category in high_level_cats:
    category_data = monthly_df[
        (monthly_df['ProductsAccordingToPRODCOMList'] == category) & 
        (monthly_df['OutputAndImportPrices'] == 'Total sales')
    ]
    
    if len(category_data) > 0:
        # Sort by date to ensure proper line plotting
        category_data = category_data.sort_values('Date')
        
        plt.plot(
            category_data['Date'], 
            category_data['PriceIndexNumbersExcludingExcise_1'],
            label=category,
            linewidth=2
        )

# Add title and labels
plt.title('Producer Price Index by Product Category (2015=100)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Price Index (2015=100)', fontsize=12)
plt.legend(title='Product Category', fontsize=10)

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
plt.xticks(rotation=45)

# Add grid for better readability
plt.grid(True, alpha=0.3)

# Add a horizontal line at 100 (the base year 2015)
plt.axhline(y=100, color='gray', linestyle='--', alpha=0.7)

# Add annotations for key events
plt.annotate('COVID-19\nPandemic', xy=(datetime(2020, 3, 1), 80), xytext=(datetime(2020, 1, 1), 50),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=10)

plt.annotate('Energy Crisis\n2021-2022', xy=(datetime(2022, 1, 1), 350), xytext=(datetime(2021, 6, 1), 300),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=10)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170512_producer_prices_easy/visualization.png', dpi=300)