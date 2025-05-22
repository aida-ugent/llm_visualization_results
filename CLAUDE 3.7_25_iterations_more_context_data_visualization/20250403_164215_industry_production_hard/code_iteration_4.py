# Automatically saved code from agent execution
# Run ID: 20250403_164215_industry_production_hard, Iteration: 4

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv')

# Filter for the specific sector and date range
sector_filter = df['SectorBranchesSIC2008'] == '16 Manufacture of wood products'

# Convert 'Periods' to datetime for proper filtering and plotting
def parse_period(period_str):
    parts = period_str.split()
    if len(parts) == 2:  # Format: "2020 January"
        return datetime.strptime(period_str, '%Y %B')
    else:  # Format: "2020 1st quarter"
        return None  # We'll filter these out

# Apply the parsing function
df['Date'] = df['Periods'].apply(parse_period)
df = df.dropna(subset=['Date'])  # Remove rows where Date couldn't be parsed

# Filter for 2020-2021
start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 12, 31)
date_filter = (df['Date'] >= start_date) & (df['Date'] <= end_date)

# Apply both filters
filtered_df = df[sector_filter & date_filter].copy()

# Sort by date
filtered_df = filtered_df.sort_values('Date')

# Check if we have data
print(f"Number of data points for {filtered_df['SectorBranchesSIC2008'].iloc[0]} in 2020-2021: {len(filtered_df)}")

# Create the plot
plt.figure(figsize=(12, 7))
sns.set_style("whitegrid")

# Plot the seasonally adjusted daily turnover for domestic and foreign markets
plt.plot(filtered_df['Date'], filtered_df['SeasonallyAdjDailyTurnoverDomestic_11'], 
         marker='o', linestyle='-', color='#1f77b4', label='Domestic Market')
plt.plot(filtered_df['Date'], filtered_df['SeasonallyAdjDailyTurnoverForeign_12'], 
         marker='s', linestyle='-', color='#ff7f0e', label='Foreign Market')

# Format the x-axis to show months
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.gcf().autofmt_xdate()  # Rotate date labels

# Add labels and title
plt.title('Seasonally Adjusted Daily Turnover for Wood Products Manufacturing (2020-2021)', 
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12, labelpad=10)
plt.ylabel('Turnover Index', fontsize=12, labelpad=10)

# Add a grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend(title='Market', title_fontsize=12, fontsize=10, loc='best')

# Add annotations for context
min_date = filtered_df['Date'].min().strftime('%b %Y')
max_date = filtered_df['Date'].max().strftime('%b %Y')
plt.figtext(0.5, 0.01, 
            f"Period: {min_date} to {max_date}\nSector: 16 Manufacture of wood products", 
            ha='center', fontsize=10, style='italic')

# Ensure the layout is tight
plt.tight_layout(rect=[0, 0.03, 1, 0.97])

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164215_industry_production_hard/visualization.png', dpi=300)

# Print some statistics for context
print("\nStatistics for Domestic Market:")
print(filtered_df['SeasonallyAdjDailyTurnoverDomestic_11'].describe())
print("\nStatistics for Foreign Market:")
print(filtered_df['SeasonallyAdjDailyTurnoverForeign_12'].describe())