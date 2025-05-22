# Automatically saved code from agent execution
# Run ID: 20250403_164105_industry_production_medium, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Set the style for the plot
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

# Load the data
data = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv')

# Filter for 'B Mining and quarrying' sector
mining_data = data[data['SectorBranchesSIC2008'] == 'B Mining and quarrying']

# Convert 'Periods' to datetime for better plotting
# The format appears to be 'YYYY Month'
mining_data['Date'] = pd.to_datetime(mining_data['Periods'], format='%Y %B')

# Sort by date to ensure chronological order
mining_data = mining_data.sort_values('Date')

# Plot the seasonally adjusted daily turnover for foreign markets
plt.plot(mining_data['Date'], mining_data['SeasonallyAdjDailyTurnoverForeign_12'], 
         marker='o', markersize=3, linestyle='-', linewidth=1.5, color='#1f77b4')

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years

# Add labels and title
plt.xlabel('Year', fontsize=12)
plt.ylabel('Seasonally Adjusted Daily Turnover (Foreign Markets)', fontsize=12)
plt.title('Seasonally Adjusted Daily Turnover for Foreign Markets\nB Mining and Quarrying (2005-2023)', fontsize=14)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164105_industry_production_medium/visualization.png', dpi=300)