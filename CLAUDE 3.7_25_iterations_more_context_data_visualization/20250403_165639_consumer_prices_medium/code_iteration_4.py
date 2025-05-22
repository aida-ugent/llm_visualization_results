# Automatically saved code from agent execution
# Run ID: 20250403_165639_consumer_prices_medium, Iteration: 4

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Filter for the specific category
category = '011120 Flours and other cereals'
filtered_df = df[df['ExpenditureCategories'] == category]

# Convert the 'Periods' column to datetime for better plotting
def parse_period(period):
    parts = period.split()
    if len(parts) == 2:
        year, month = parts
        # Convert month name to month number
        month_dict = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04',
            'May': '05', 'June': '06', 'July': '07', 'August': '08',
            'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }
        month_num = month_dict.get(month, '01')
        return f"{year}-{month_num}-01"
    else:
        # If only year is provided, use January 1st of that year
        return f"{period}-01-01"

filtered_df['Date'] = filtered_df['Periods'].apply(parse_period)
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

# Sort by date
filtered_df = filtered_df.sort_values('Date')

# Print some debug info
print(f"Found {len(filtered_df)} records for category '{category}'")
if len(filtered_df) == 0:
    # Let's check what categories are available
    print("Available categories:")
    print(df['ExpenditureCategories'].unique()[:20])  # Print first 20 categories

# Create the plot
plt.figure(figsize=(12, 6))

if len(filtered_df) > 0:
    plt.plot(filtered_df['Date'], filtered_df['DerivedCPI_2'], marker='', linewidth=2, color='#1f77b4')

    # Add title and labels
    plt.title(f'Derived Consumer Price Index (CPI) for "{category}"', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Derived CPI', fontsize=12)

    # Format the x-axis to show years
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years

    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Add a note about the data source
    plt.figtext(0.5, 0.01, 'Source: Consumer Prices Dataset', ha='center', fontsize=10)
else:
    plt.text(0.5, 0.5, f"No data found for category '{category}'", 
             horizontalalignment='center', verticalalignment='center',
             transform=plt.gca().transAxes, fontsize=14)

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165639_consumer_prices_medium/visualization.png', dpi=300, bbox_inches='tight')