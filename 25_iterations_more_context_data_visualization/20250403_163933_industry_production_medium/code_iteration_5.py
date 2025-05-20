# Automatically saved code from agent execution
# Run ID: 20250403_163933_industry_production_medium, Iteration: 5

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

# Let's check the data for NaN values in the turnover columns
print("Total NaN values in DomesticTurnover_5:", df['DomesticTurnover_5'].isna().sum())
print("Total NaN values in ForeignTurnover_6:", df['ForeignTurnover_6'].isna().sum())
print("Total rows:", len(df))

# Instead of focusing on just one sector, let's aggregate data across all sectors
# First, convert periods to datetime for better plotting
df['Date'] = pd.to_datetime(df['Periods'], format='%Y %B', errors='coerce')

# Group by date and calculate mean turnover values for each month
# This will give us an overall picture across all sectors
monthly_data = df.groupby('Date').agg({
    'DomesticTurnover_5': 'mean',
    'ForeignTurnover_6': 'mean'
}).reset_index()

# Sort by date
monthly_data = monthly_data.sort_values('Date')

# Check the aggregated data
print("\nAggregated monthly data shape:", monthly_data.shape)
print("First few rows of aggregated data:")
print(monthly_data.head())

# Create the plot
plt.figure(figsize=(12, 7))

# Plot domestic and foreign turnover
plt.plot(monthly_data['Date'], monthly_data['DomesticTurnover_5'], 
         label='Domestic Turnover', linewidth=2, color='#1f77b4')
plt.plot(monthly_data['Date'], monthly_data['ForeignTurnover_6'], 
         label='Foreign Turnover', linewidth=2, color='#ff7f0e')

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years

# Add labels and title
plt.xlabel('Year', fontsize=12)
plt.ylabel('Turnover Index (Average across all sectors)', fontsize=12)
plt.title('Comparison of Domestic vs Foreign Turnover\nAverage across All Industry Sectors', 
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

print("\nPlot saved successfully!")