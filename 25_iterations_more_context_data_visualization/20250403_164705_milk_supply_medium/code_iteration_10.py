# Automatically saved code from agent execution
# Run ID: 20250403_164705_milk_supply_medium, Iteration: 10

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from scipy import stats

# Set the style for the plot
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

# Load the data
file_path = '/Users/alexanderrogiers/ugent/llm_visualization/data/milk_production_1.csv'
df = pd.read_csv(file_path)

# Extract year from the 'Periods' column
df['Year'] = df['Periods'].str.extract(r'(\d{4})').astype(int)

# Extract month from the 'Periods' column
# Create a mapping for month names to numbers
month_map = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}

# Extract month name and map to number
df['Month'] = df['Periods'].str.extract(r'(\w+)$')[0].map(month_map)

# Create a date column using year and month
df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(Day=1))

# Filter for the years 2010-2015
filtered_df = df[(df['Year'] >= 2010) & (df['Year'] <= 2015)].copy()

# Drop any rows with NaT dates
filtered_df = filtered_df.dropna(subset=['Date'])

# Sort by date to ensure proper plotting
filtered_df = filtered_df.sort_values('Date')

# Create a numerical representation of the date for trend line calculation
filtered_df['date_ordinal'] = pd.to_datetime(filtered_df['Date']).map(mdates.date2num)

# Calculate trend line
slope, intercept, r_value, p_value, std_err = stats.linregress(filtered_df['date_ordinal'], filtered_df['Volume_1'])
trend_line = slope * filtered_df['date_ordinal'] + intercept

# Plot the data
plt.plot(filtered_df['Date'], filtered_df['Volume_1'], marker='o', linestyle='-', color='#1f77b4', linewidth=1.5, markersize=4, label='Monthly Volume')

# Plot the trend line
plt.plot(filtered_df['Date'], trend_line, 'r--', linewidth=1.5, label=f'Trend (R² = {r_value**2:.2f})')

# Format the x-axis to show months and years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Show every 3 months
plt.gcf().autofmt_xdate()  # Rotate date labels

# Format y-axis with thousands separator
from matplotlib.ticker import FuncFormatter
def thousands_formatter(x, pos):
    return f'{int(x):,}'
plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.title('Monthly Volume of Raw Cow\'s Milk Delivered by Dairy Farmers (2010-2015)', fontsize=14, pad=20)
plt.xlabel('Month', fontsize=12, labelpad=10)
plt.ylabel('Volume (in tons)', fontsize=12, labelpad=10)

# Add legend
plt.legend(loc='lower right')

# Find the maximum and minimum points
max_idx = filtered_df['Volume_1'].idxmax()
max_value = filtered_df.loc[max_idx, 'Volume_1']
max_date = filtered_df.loc[max_idx, 'Date']

min_idx = filtered_df['Volume_1'].idxmin()
min_value = filtered_df.loc[min_idx, 'Volume_1']
min_date = filtered_df.loc[min_idx, 'Date']

# Annotate maximum and minimum points
plt.annotate(f'Max: {int(max_value):,} tons', 
             xy=(max_date, max_value),
             xytext=(max_date, max_value + 30000),
             ha='center', va='bottom',
             arrowprops=dict(arrowstyle='->', color='green', lw=1),
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.8))

plt.annotate(f'Min: {int(min_value):,} tons', 
             xy=(min_date, min_value),
             xytext=(min_date, min_value - 30000),
             ha='center', va='top',
             arrowprops=dict(arrowstyle='->', color='red', lw=1),
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", alpha=0.8))

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add a subtle background color to enhance readability
plt.gca().set_facecolor('#f8f9fa')

# Add text about key observations
plt.figtext(0.5, 0.01, 
            "Observations: 1) Clear upward trend from 2010 to 2015  2) Seasonal patterns visible throughout each year  3) Significant increase after 2014",
            ha="center", fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164705_milk_supply_medium/visualization.png', dpi=300, bbox_inches='tight')

# Close the plot to free memory
plt.close()