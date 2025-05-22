# Automatically saved code from agent execution
# Run ID: 20250403_164537_milk_supply_easy, Iteration: 5

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np

# Set the style for the plot
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

# Load the data
data_path = '/Users/alexanderrogiers/ugent/llm_visualization/data/milk_production_1.csv'
df = pd.read_csv(data_path)

# Convert 'Periods' to datetime for better plotting
# Extract year and month from the 'Periods' column
df['Year'] = df['Periods'].str.extract(r'^(\d{4})').astype(int)

# Identify if the period is a month or a year
df['is_month'] = df['Periods'].str.contains(' ')

# For monthly data, extract the month
month_dict = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}

def extract_month(period):
    if ' ' in period:
        month_name = period.split(' ')[1]
        return month_dict.get(month_name, 1)
    return 0  # For yearly data

df['Month'] = df['Periods'].apply(extract_month)

# Create a proper date column
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-15', 
                           format='%Y-%m-%d', errors='coerce')

# For yearly data, set date to middle of the year
yearly_mask = ~df['is_month']
df.loc[yearly_mask, 'Date'] = pd.to_datetime(df.loc[yearly_mask, 'Year'].astype(str) + '-07-01')

# Sort by date to ensure chronological order
df = df.sort_values('Date')

# Separate monthly and yearly data
monthly_data = df[df['is_month']]
yearly_data = df[~df['is_month']]

# Plot the monthly cheese production
plt.plot(monthly_data['Date'], monthly_data['Cheese_5'], color='#f9a825', linewidth=1.5, 
         label='Monthly Production')

# Plot the yearly cheese production with markers
if not yearly_data.empty:
    plt.plot(yearly_data['Date'], yearly_data['Cheese_5'], color='#e65100', linewidth=2.5,
             marker='o', markersize=8, label='Annual Production')

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years
plt.xticks(rotation=45)

# Add labels and title
plt.xlabel('Year', fontsize=12)
plt.ylabel('Cheese Production Volume (tons)', fontsize=12)
plt.title('Cheese Production Volume in the Netherlands (1995-present)', fontsize=14, fontweight='bold')

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend(loc='upper left')

# Annotate the most recent data point
last_yearly_point = yearly_data.iloc[-1] if not yearly_data.empty else None
if last_yearly_point is not None:
    plt.annotate(f'Latest Annual: {int(last_yearly_point["Cheese_5"]):,} tons',
                xy=(last_yearly_point['Date'], last_yearly_point['Cheese_5']),
                xytext=(10, -20),
                textcoords='offset points',
                fontsize=10,
                fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#e65100'))

# Enhance the plot with a light background to improve contrast
plt.gca().set_facecolor('#f8f9fa')

# Add a subtle border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_color('#dddddd')
plt.gca().spines['bottom'].set_color('#dddddd')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the figure
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164537_milk_supply_easy/visualization.png', dpi=300, bbox_inches='tight')