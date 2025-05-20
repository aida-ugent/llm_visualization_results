# Automatically saved code from agent execution
# Run ID: 20250403_164105_industry_production_medium, Iteration: 6

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import re
import numpy as np

# Set the style for the plot
sns.set_style("whitegrid")
plt.figure(figsize=(12, 7))

# Load the data
data = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv')

# Filter for 'B Mining and quarrying' sector
mining_data = data[data['SectorBranchesSIC2008'] == 'B Mining and quarrying'].copy()

# Custom function to convert period strings to datetime
def convert_period_to_date(period_str):
    # Check if it's a quarterly period
    if 'quarter' in period_str.lower():
        year = int(period_str.split()[0])
        quarter = int(re.search(r'(\d+)', period_str.split()[1]).group(1))
        # Map quarter to middle month of the quarter
        month = 3 * quarter - 1
        return pd.Timestamp(year=year, month=month, day=15)
    else:
        # For monthly data
        try:
            return pd.to_datetime(period_str, format='%Y %B')
        except:
            # For yearly data or other formats
            try:
                year = int(period_str.split()[0])
                return pd.Timestamp(year=year, month=6, day=30)  # Middle of the year
            except:
                return pd.NaT

# Apply the conversion function
mining_data['Date'] = mining_data['Periods'].apply(convert_period_to_date)

# Drop rows with NaT dates
mining_data = mining_data.dropna(subset=['Date'])

# Sort by date to ensure chronological order
mining_data = mining_data.sort_values('Date')

# Calculate 12-month moving average for trend line
mining_data['MA_12'] = mining_data['SeasonallyAdjDailyTurnoverForeign_12'].rolling(window=12, min_periods=1).mean()

# Plot the seasonally adjusted daily turnover for foreign markets
plt.plot(mining_data['Date'], mining_data['SeasonallyAdjDailyTurnoverForeign_12'], 
         marker='o', markersize=3, linestyle='-', linewidth=1.2, color='#1f77b4', alpha=0.8,
         label='Monthly Values')

# Add the moving average trend line
plt.plot(mining_data['Date'], mining_data['MA_12'], 
         linestyle='-', linewidth=2.5, color='#d62728', alpha=0.9,
         label='12-Month Moving Average')

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years

# Add labels and title
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Index Value', fontsize=12, fontweight='bold')
plt.title('Seasonally Adjusted Daily Turnover for Foreign Markets\nB Mining and Quarrying (2005-2023)', 
          fontsize=16, fontweight='bold', pad=15)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add legend
plt.legend(loc='upper right', frameon=True, framealpha=0.9)

# Add annotations for key events
plt.annotate('Global Financial\nCrisis', xy=(pd.Timestamp('2008-09-15'), 100), 
             xytext=(pd.Timestamp('2008-06-01'), 130),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8, alpha=0.7),
             fontsize=10, fontweight='bold')

plt.annotate('COVID-19\nPandemic', xy=(pd.Timestamp('2020-03-15'), 40), 
             xytext=(pd.Timestamp('2020-01-01'), 80),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8, alpha=0.7),
             fontsize=10, fontweight='bold')

plt.annotate('2022 Energy\nCrisis Peak', xy=(pd.Timestamp('2022-06-15'), 240), 
             xytext=(pd.Timestamp('2022-03-01'), 190),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8, alpha=0.7),
             fontsize=10, fontweight='bold')

# Add a subtle background color
plt.gca().set_facecolor('#f8f9fa')

# Add a note about the data source
plt.figtext(0.5, 0.01, 'Data Source: Statistics Netherlands (CBS)', 
            ha='center', fontsize=9, style='italic')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164105_industry_production_medium/visualization.png', 
            dpi=300, bbox_inches='tight')