# Automatically saved code from agent execution
# Run ID: 20250403_165639_consumer_prices_medium, Iteration: 8

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Filter for the specific category
category = '011120 Flours and other cereals'
filtered_df = df[df['ExpenditureCategories'] == category].copy()  # Use copy to avoid SettingWithCopyWarning

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

# Check the date range
print(f"Date range: {filtered_df['Date'].min()} to {filtered_df['Date'].max()}")

# Create the plot with a specific style
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(14, 8))

# Plot the data with a thicker line
ax.plot(filtered_df['Date'], filtered_df['DerivedCPI_2'], 
        linewidth=2.5, color='#1f77b4', label='Derived CPI')

# Add a trend line (12-month moving average)
filtered_df['MA_12'] = filtered_df['DerivedCPI_2'].rolling(window=12).mean()
ax.plot(filtered_df['Date'], filtered_df['MA_12'], 
        linewidth=2, color='#ff7f0e', linestyle='--', 
        label='12-Month Moving Average')

# Highlight significant events or periods
# Find the maximum value and its date
max_cpi = filtered_df['DerivedCPI_2'].max()
max_date = filtered_df.loc[filtered_df['DerivedCPI_2'] == max_cpi, 'Date'].iloc[0]

# Find the start of the sharp increase (around 2021)
# Let's find a more precise point - where the increase starts to accelerate
# We'll use the point where the year-on-year change exceeds 5%
filtered_df['YoY_Change'] = filtered_df['DerivedCPI_2'].pct_change(periods=12) * 100
sharp_increase_idx = filtered_df[(filtered_df['Date'] >= '2021-01-01') & 
                                (filtered_df['YoY_Change'] > 5)].index.min()

if pd.notna(sharp_increase_idx):
    start_increase = filtered_df.loc[sharp_increase_idx]
    
    # Annotate the start of the sharp increase
    ax.annotate('Sharp price increase\nbegins', 
                xy=(start_increase['Date'], start_increase['DerivedCPI_2']),
                xytext=(start_increase['Date'] - pd.Timedelta(days=180), 
                       start_increase['DerivedCPI_2'] - 10),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                fontsize=10, fontweight='bold')

# Annotate the maximum point
ax.annotate(f'Peak: {max_cpi:.1f}', 
            xy=(max_date, max_cpi),
            xytext=(max_date - pd.Timedelta(days=180), max_cpi + 3),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
            fontsize=10, fontweight='bold')

# Add title and labels with better formatting
ax.set_title(f'Derived Consumer Price Index (CPI) for "{category}"', 
             fontsize=16, pad=20, fontweight='bold')
ax.set_xlabel('Year', fontsize=14, labelpad=10)
ax.set_ylabel('Derived CPI', fontsize=14, labelpad=10)

# Format the x-axis to show years
years = mdates.YearLocator(2)  # Show every 2 years
years_fmt = mdates.DateFormatter('%Y')
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)

# Set x-axis limits to ensure we see the full date range
ax.set_xlim(filtered_df['Date'].min() - pd.Timedelta(days=30), 
           filtered_df['Date'].max() + pd.Timedelta(days=30))

# Add a horizontal line at y=100 for reference (base index)
ax.axhline(y=100, color='gray', linestyle='-', alpha=0.3, linewidth=1)
ax.text(filtered_df['Date'].min() + pd.Timedelta(days=30), 100.5, 'Base Reference (100)', 
        fontsize=9, color='gray')

# Set y-axis limits with some padding
y_min = max(95, filtered_df['DerivedCPI_2'].min() - 5)
y_max = filtered_df['DerivedCPI_2'].max() + 5
ax.set_ylim(y_min, y_max)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add grid for better readability (lighter)
ax.grid(True, linestyle='--', alpha=0.6)

# Add legend
ax.legend(loc='lower right', frameon=True, fontsize=12)

# Add a note about the data source and a brief explanation
footnote = ('Source: Consumer Prices Dataset\n'
            'Note: The Derived CPI excludes the effect of changes in product-related taxes and subsidies.')
plt.figtext(0.5, 0.01, footnote, ha='center', fontsize=10, 
            bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

# Add a subtle background color to the plot area
ax.set_facecolor('#f8f9fa')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot with high resolution
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165639_consumer_prices_medium/visualization.png', 
            dpi=300, bbox_inches='tight')