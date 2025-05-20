# Automatically saved code from agent execution
# Run ID: 20250403_163805_industry_production_easy, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Load the data
data = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv')

# Convert 'Periods' to datetime for better plotting
# First, standardize the format
data['Periods'] = data['Periods'].str.replace(' ', '-')
data['Periods'] = pd.to_datetime(data['Periods'], format='%Y-%B', errors='coerce')

# Sort by date
data = data.sort_values('Periods')

# Filter for unique sectors
sectors = data['SectorBranchesSIC2008'].unique()

# Create a figure with appropriate size
plt.figure(figsize=(14, 8))

# Plot foreign turnover for each sector
for sector in sectors:
    sector_data = data[data['SectorBranchesSIC2008'] == sector]
    plt.plot(sector_data['Periods'], sector_data['ForeignTurnover_6'], 
             label=sector, linewidth=1.5, alpha=0.8)

# Format the plot
plt.title('Foreign Turnover Across All Periods by Sector', fontsize=16)
plt.xlabel('Time Period', fontsize=12)
plt.ylabel('Foreign Turnover', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Format x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years
plt.xticks(rotation=45)

# Add legend with smaller font outside the plot
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# Adjust layout to make room for the legend
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_163805_industry_production_easy/visualization.png', 
            dpi=300, bbox_inches='tight')

plt.close()