# Automatically saved code from agent execution
# Run ID: 20250403_163805_industry_production_easy, Iteration: 7

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

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
plt.figure(figsize=(14, 10))

# Create a custom colormap for better distinction
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Plot foreign turnover for top sectors with rolling average
for i, sector in enumerate(top_sectors):
    sector_data = data[data['SectorBranchesSIC2008'] == sector].copy()
    
    # Calculate 12-month rolling average
    sector_data = sector_data.sort_values('Periods')
    sector_data['RollingAvg'] = sector_data['ForeignTurnover_6'].rolling(window=12, min_periods=1).mean()
    
    # Plot both the raw data (lighter) and rolling average (darker)
    plt.plot(sector_data['Periods'], sector_data['ForeignTurnover_6'], 
             color=colors[i], alpha=0.3, linewidth=1)
    plt.plot(sector_data['Periods'], sector_data['RollingAvg'], 
             color=colors[i], label=sector, linewidth=2.5)

# Format the plot
plt.title('Foreign Turnover Trends (2005-2023) - Top 5 Sectors', fontsize=18, pad=20)
plt.xlabel('Year', fontsize=14, labelpad=10)
plt.ylabel('Foreign Turnover Index', fontsize=14, labelpad=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Format x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# Add legend with reasonable font size
plt.legend(loc='upper left', fontsize=12, framealpha=0.9)

# Annotate key events
plt.axvspan(pd.to_datetime('2008-09-01'), pd.to_datetime('2009-06-01'), 
            alpha=0.2, color='gray', label='Global Financial Crisis')
plt.axvspan(pd.to_datetime('2020-03-01'), pd.to_datetime('2020-12-01'), 
            alpha=0.2, color='gray', label='COVID-19 Pandemic')

# Add text annotations
plt.annotate('Financial Crisis', xy=(pd.to_datetime('2008-12-01'), 50), 
             xytext=(pd.to_datetime('2008-12-01'), 20),
             fontsize=10, ha='center', color='dimgray')
plt.annotate('COVID-19', xy=(pd.to_datetime('2020-06-01'), 50), 
             xytext=(pd.to_datetime('2020-06-01'), 20),
             fontsize=10, ha='center', color='dimgray')
plt.annotate('Post-COVID Recovery', xy=(pd.to_datetime('2021-06-01'), 200), 
             xytext=(pd.to_datetime('2021-06-01'), 230),
             fontsize=10, ha='center', color='dimgray',
             arrowprops=dict(arrowstyle='->', color='dimgray'))

# Add a note about the visualization
plt.figtext(0.5, 0.01, 
            'Note: Showing the 5 sectors with highest average foreign turnover. Lighter lines show raw data; darker lines show 12-month rolling averages.', 
            ha='center', fontsize=10, style='italic')

# Set y-axis limits to better show the data
plt.ylim(0, 300)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_163805_industry_production_easy/visualization.png', 
            dpi=300, bbox_inches='tight')

plt.close()