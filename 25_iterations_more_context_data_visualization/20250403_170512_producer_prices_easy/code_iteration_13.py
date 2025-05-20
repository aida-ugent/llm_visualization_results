# Automatically saved code from agent execution
# Run ID: 20250403_170512_producer_prices_easy, Iteration: 13

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from matplotlib.ticker import MaxNLocator

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

# Find all high-level categories (starting with a letter)
high_level_cats = [cat for cat in monthly_df['ProductsAccordingToPRODCOMList'].unique() 
                  if isinstance(cat, str) and cat[0].isalpha() and cat[1] == ' ']

# Create a figure with a single plot
plt.figure(figsize=(14, 8))

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
            linewidth=2.5
        )

# Add title and labels
plt.title('Producer Price Index Excluding Excise Taxes (2015=100)', fontsize=18, fontweight='bold')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Price Index (2015=100)', fontsize=14)
plt.legend(title='Product Category', fontsize=12, title_fontsize=13)

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)

# Add grid for better readability
plt.grid(True, alpha=0.3)

# Add a horizontal line at 100 (the base year 2015)
plt.axhline(y=100, color='gray', linestyle='--', alpha=0.7, label='Base Year (2015=100)')

# Add annotations for key events
plt.annotate('COVID-19 Pandemic\nPrice Drop', xy=(datetime(2020, 4, 1), 70), xytext=(datetime(2019, 7, 1), 50),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=12)

plt.annotate('Energy Crisis\n2021-2022', xy=(datetime(2022, 1, 1), 350), xytext=(datetime(2021, 3, 1), 280),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=12)

plt.annotate('Mining prices\nstabilizing', xy=(datetime(2023, 6, 1), 220), xytext=(datetime(2023, 8, 1), 260),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=12)

# Add a text box with key insights
textstr = '\n'.join((
    'Key Insights:',
    '• Mining prices show extreme volatility (2020-2023)',
    '• Manufacturing prices more stable but still rising',
    '• Both sectors above 2015 baseline in 2023',
    '• Mining prices peaked at 450% of 2015 levels during energy crisis'
))

props = dict(boxstyle='round', facecolor='white', alpha=0.7)
plt.text(0.02, 0.02, textstr, transform=plt.gca().transAxes, fontsize=12,
        verticalalignment='bottom', bbox=props)

# Set y-axis limits to better show the data
plt.ylim(40, 470)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170512_producer_prices_easy/visualization.png', dpi=300)