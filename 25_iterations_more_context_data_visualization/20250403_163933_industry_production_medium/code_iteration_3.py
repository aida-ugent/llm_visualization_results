# Automatically saved code from agent execution
# Run ID: 20250403_163933_industry_production_medium, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns

# Set the style
plt.style.use('seaborn-v0_8-whitegrid')

# Load the data
file_path = '/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv'
df = pd.read_csv(file_path)

# Check if "All sectors" exists in the data
print("Unique sectors in the dataset:")
print(df['SectorBranchesSIC2008'].unique())

# Filter for "All sectors" or equivalent
# Based on the dataset description, we need to find the right category name
all_sectors = df[df['SectorBranchesSIC2008'] == 'B-E Industry (no construction)']

# If "All sectors" doesn't exist with that exact name, let's find an alternative
if len(all_sectors) == 0:
    # Look for a category that might represent all sectors
    potential_all_sectors = [s for s in df['SectorBranchesSIC2008'].unique() 
                            if 'all' in s.lower() or 'total' in s.lower() or 'industry' in s.lower()]
    print("Potential 'all sectors' categories:", potential_all_sectors)
    
    if potential_all_sectors:
        all_sectors = df[df['SectorBranchesSIC2008'] == potential_all_sectors[0]]
    else:
        # If no clear "all sectors" category, use the first category as an example
        print("No clear 'all sectors' category found. Using the first category as an example.")
        all_sectors = df[df['SectorBranchesSIC2008'] == df['SectorBranchesSIC2008'].unique()[0]]

# Convert periods to datetime for better plotting
all_sectors['Date'] = pd.to_datetime(all_sectors['Periods'], format='%Y %B', errors='coerce')

# Sort by date
all_sectors = all_sectors.sort_values('Date')

# Create the plot
plt.figure(figsize=(12, 7))

# Plot domestic and foreign turnover
plt.plot(all_sectors['Date'], all_sectors['DomesticTurnover_5'], 
         label='Domestic Turnover', linewidth=2, color='#1f77b4')
plt.plot(all_sectors['Date'], all_sectors['ForeignTurnover_6'], 
         label='Foreign Turnover', linewidth=2, color='#ff7f0e')

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years

# Add labels and title
plt.xlabel('Year', fontsize=12)
plt.ylabel('Turnover Index', fontsize=12)
plt.title(f'Comparison of Domestic vs Foreign Turnover\n{all_sectors["SectorBranchesSIC2008"].iloc[0]}', 
          fontsize=14, fontweight='bold')

# Add legend
plt.legend(fontsize=12)

# Add grid for better readability
plt.grid(True, alpha=0.3)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Tight layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_163933_industry_production_medium/visualization.png', dpi=300)

print("Plot saved successfully!")