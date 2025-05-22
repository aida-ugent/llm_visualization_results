# Automatically saved code from agent execution
# Run ID: 20250403_164537_milk_supply_easy, Iteration: 7

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

# Extract year from the 'Periods' column
df['Year'] = df['Periods'].str.extract(r'^(\d{4})').astype(int)

# Identify if the period is a month or a year
df['is_month'] = df['Periods'].str.contains(' ')

# Filter to get only yearly data for a cleaner visualization
yearly_data = df[~df['is_month']].copy()

# Create a proper date column for yearly data
yearly_data['Date'] = pd.to_datetime(yearly_data['Year'].astype(str) + '-07-01')

# Sort by date to ensure chronological order
yearly_data = yearly_data.sort_values('Date')

# Plot the yearly cheese production
plt.figure(figsize=(12, 7))

# Create the line plot with markers
plt.plot(yearly_data['Date'], yearly_data['Cheese_5'], color='#e65100', linewidth=2.5,
         marker='o', markersize=8, label='Annual Cheese Production')

# Add a trend line to highlight the overall pattern
z = np.polyfit(range(len(yearly_data)), yearly_data['Cheese_5'], 1)
p = np.poly1d(z)
plt.plot(yearly_data['Date'], p(range(len(yearly_data))), 
         linestyle='--', color='#1976d2', linewidth=1.5, 
         label=f'Trend Line (Slope: {z[0]:.0f} tons/year)')

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years
plt.xticks(rotation=45)

# Add labels and title
plt.xlabel('Year', fontsize=12)
plt.ylabel('Cheese Production Volume (tons)', fontsize=12)
plt.title('Annual Cheese Production Volume in the Netherlands (1995-present)', 
          fontsize=16, fontweight='bold', pad=20)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend(loc='upper left', fontsize=10)

# Annotate the first and last data points
first_point = yearly_data.iloc[0]
last_point = yearly_data.iloc[-1]

plt.annotate(f'{first_point["Year"]}: {int(first_point["Cheese_5"]):,} tons',
            xy=(first_point['Date'], first_point['Cheese_5']),
            xytext=(-10, -30),
            textcoords='offset points',
            fontsize=10,
            arrowprops=dict(arrowstyle='->', color='#555555'))

plt.annotate(f'{last_point["Year"]}: {int(last_point["Cheese_5"]):,} tons',
            xy=(last_point['Date'], last_point['Cheese_5']),
            xytext=(10, -30),
            textcoords='offset points',
            fontsize=10,
            fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#e65100'))

# Calculate and display the percentage increase
percent_increase = ((last_point['Cheese_5'] - first_point['Cheese_5']) / first_point['Cheese_5']) * 100
plt.figtext(0.5, 0.01, 
            f"Overall increase from {first_point['Year']} to {last_point['Year']}: {percent_increase:.1f}%",
            ha='center', fontsize=12, bbox=dict(facecolor='#f0f0f0', alpha=0.5, boxstyle='round,pad=0.5'))

# Enhance the plot with a light background to improve contrast
plt.gca().set_facecolor('#f8f9fa')

# Add a subtle border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_color('#dddddd')
plt.gca().spines['bottom'].set_color('#dddddd')

# Set y-axis to start from 0 to avoid misleading visualization
plt.ylim(bottom=0)

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the figure
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164537_milk_supply_easy/visualization.png', dpi=300, bbox_inches='tight')