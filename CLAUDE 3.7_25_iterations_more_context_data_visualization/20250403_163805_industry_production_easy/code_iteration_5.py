# Automatically saved code from agent execution
# Run ID: 20250403_163805_industry_production_easy, Iteration: 5

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Load the data
data = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv')

# Convert 'Periods' to datetime for better plotting
data['Periods'] = data['Periods'].str.replace(' ', '-')
data['Periods'] = pd.to_datetime(data['Periods'], format='%Y-%B', errors='coerce')

# Sort by date
data = data.sort_values('Periods')

# Calculate average foreign turnover for each sector
sector_avg = data.groupby('SectorBranchesSIC2008')['ForeignTurnover_6'].mean().sort_values(ascending=False)

# Get top 5 sectors with highest average foreign turnover
top_sectors = sector_avg.head(5).index.tolist()

# Create a figure with appropriate size
plt.figure(figsize=(14, 8))

# Plot foreign turnover for top sectors
for sector in top_sectors:
    sector_data = data[data['SectorBranchesSIC2008'] == sector]
    plt.plot(sector_data['Periods'], sector_data['ForeignTurnover_6'], 
             label=sector, linewidth=2, alpha=0.8)

# Format the plot
plt.title('Foreign Turnover Across All Periods - Top 5 Sectors', fontsize=16)
plt.xlabel('Time Period', fontsize=12)
plt.ylabel('Foreign Turnover', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Format x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years
plt.xticks(rotation=45)

# Add legend with reasonable font size
plt.legend(loc='best', fontsize=10)

# Add a note about the selection criteria
plt.figtext(0.5, 0.01, 'Note: Showing the 5 sectors with highest average foreign turnover', 
            ha='center', fontsize=10, style='italic')

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_163805_industry_production_easy/visualization.png', 
            dpi=300, bbox_inches='tight')

plt.close()