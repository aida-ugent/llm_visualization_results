# Automatically saved code from agent execution
# Run ID: 20250403_164215_industry_production_hard, Iteration: 6

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
import numpy as np

# Set the style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("notebook", font_scale=1.1)

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv')

# Filter for the specific sector
sector_filter = df['SectorBranchesSIC2008'] == '16 Manufacture of wood products'
sector_data = df[sector_filter].copy()

# Convert 'Periods' to datetime for proper filtering and plotting
def parse_period(period_str):
    parts = period_str.split()
    if len(parts) == 2:  # Format: "2020 January"
        return datetime.strptime(period_str, '%Y %B')
    else:  # Format: "2020 1st quarter"
        return None  # We'll filter these out

# Apply the parsing function
sector_data['Date'] = sector_data['Periods'].apply(parse_period)
sector_data = sector_data.dropna(subset=['Date'])  # Remove rows where Date couldn't be parsed

# Filter for 2020-2021
start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 12, 31)
date_filter = (sector_data['Date'] >= start_date) & (sector_data['Date'] <= end_date)
filtered_df = sector_data[date_filter].copy()

# Sort by date
filtered_df = filtered_df.sort_values('Date')

# Create the plot
fig, ax = plt.subplots(figsize=(12, 7))

# Plot the seasonally adjusted daily turnover for domestic and foreign markets
domestic_line = ax.plot(filtered_df['Date'], filtered_df['SeasonallyAdjDailyTurnoverDomestic_11'], 
         marker='o', linestyle='-', linewidth=2, color='#1f77b4', label='Domestic Market')
foreign_line = ax.plot(filtered_df['Date'], filtered_df['SeasonallyAdjDailyTurnoverForeign_12'], 
         marker='s', linestyle='-', linewidth=2, color='#ff7f0e', label='Foreign Market')

# Add a light fill below each line to enhance visibility
ax.fill_between(filtered_df['Date'], filtered_df['SeasonallyAdjDailyTurnoverDomestic_11'], 
                alpha=0.1, color='#1f77b4')
ax.fill_between(filtered_df['Date'], filtered_df['SeasonallyAdjDailyTurnoverForeign_12'], 
                alpha=0.1, color='#ff7f0e')

# Format the x-axis to show months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.gcf().autofmt_xdate(rotation=30)  # Rotate date labels

# Add labels and title
plt.title('Seasonally Adjusted Daily Turnover for Wood Products Manufacturing (2020-2021)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=13, labelpad=10)
plt.ylabel('Turnover Index', fontsize=13, labelpad=10)

# Add a grid for better readability
ax.grid(True, linestyle='--', alpha=0.7)

# Add legend
legend = ax.legend(title='Market', title_fontsize=13, fontsize=12, loc='upper left')
legend.get_frame().set_alpha(0.9)

# Highlight COVID-19 impact period
covid_start = datetime(2020, 3, 1)
covid_end = datetime(2020, 6, 30)
ax.axvspan(covid_start, covid_end, alpha=0.15, color='red', label='COVID-19 First Wave')
ax.text(datetime(2020, 4, 15), 105, 'COVID-19\nFirst Wave', 
        ha='center', va='center', color='darkred', fontsize=10, fontweight='bold')

# Highlight recovery period
recovery_start = datetime(2021, 3, 1)
recovery_end = datetime(2021, 12, 31)
ax.axvspan(recovery_start, recovery_end, alpha=0.15, color='green', label='Recovery Period')
ax.text(datetime(2021, 7, 15), 105, 'Recovery Period', 
        ha='center', va='center', color='darkgreen', fontsize=10, fontweight='bold')

# Add annotations for key points
# Find the minimum point for foreign market during COVID
covid_period = (filtered_df['Date'] >= covid_start) & (filtered_df['Date'] <= covid_end)
min_foreign_covid = filtered_df[covid_period]['SeasonallyAdjDailyTurnoverForeign_12'].min()
min_foreign_covid_date = filtered_df[covid_period][filtered_df['SeasonallyAdjDailyTurnoverForeign_12'] == min_foreign_covid]['Date'].iloc[0]

# Find the maximum point for domestic market in 2021
max_domestic_2021 = filtered_df[filtered_df['Date'].dt.year == 2021]['SeasonallyAdjDailyTurnoverDomestic_11'].max()
max_domestic_2021_date = filtered_df[filtered_df['Date'].dt.year == 2021][filtered_df['SeasonallyAdjDailyTurnoverDomestic_11'] == max_domestic_2021]['Date'].iloc[0]

# Add annotations
ax.annotate(f'Lowest foreign turnover\nduring COVID: {min_foreign_covid:.1f}',
            xy=(min_foreign_covid_date, min_foreign_covid),
            xytext=(min_foreign_covid_date - pd.Timedelta(days=30), min_foreign_covid - 10),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            fontsize=10, ha='right')

ax.annotate(f'Highest domestic turnover\nin 2021: {max_domestic_2021:.1f}',
            xy=(max_domestic_2021_date, max_domestic_2021),
            xytext=(max_domestic_2021_date, max_domestic_2021 + 10),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            fontsize=10, ha='center')

# Calculate and display the percentage change from start to end
domestic_start = filtered_df.iloc[0]['SeasonallyAdjDailyTurnoverDomestic_11']
domestic_end = filtered_df.iloc[-1]['SeasonallyAdjDailyTurnoverDomestic_11']
domestic_change = ((domestic_end - domestic_start) / domestic_start) * 100

foreign_start = filtered_df.iloc[0]['SeasonallyAdjDailyTurnoverForeign_12']
foreign_end = filtered_df.iloc[-1]['SeasonallyAdjDailyTurnoverForeign_12']
foreign_change = ((foreign_end - foreign_start) / foreign_start) * 100

# Add text box with key statistics
stats_text = (f"Overall Change (Jan 2020 to Dec 2021):\n"
              f"• Domestic Market: {domestic_change:.1f}%\n"
              f"• Foreign Market: {foreign_change:.1f}%")
props = dict(boxstyle='round', facecolor='white', alpha=0.7)
ax.text(0.02, 0.02, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', bbox=props)

# Ensure the layout is tight
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164215_industry_production_hard/visualization.png', dpi=300)

# Print some additional insights
print("Key Insights:")
print(f"1. Domestic market turnover increased by {domestic_change:.1f}% from Jan 2020 to Dec 2021")
print(f"2. Foreign market turnover increased by {foreign_change:.1f}% from Jan 2020 to Dec 2021")
print(f"3. Lowest foreign market turnover during COVID first wave: {min_foreign_covid:.1f}")
print(f"4. Highest domestic market turnover in 2021: {max_domestic_2021:.1f}")

# Calculate correlation between domestic and foreign markets
correlation = filtered_df['SeasonallyAdjDailyTurnoverDomestic_11'].corr(filtered_df['SeasonallyAdjDailyTurnoverForeign_12'])
print(f"5. Correlation between domestic and foreign markets: {correlation:.2f}")