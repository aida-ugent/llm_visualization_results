# Automatically saved code from agent execution
# Run ID: 20250403_163933_industry_production_medium, Iteration: 7

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Set the style
plt.style.use('seaborn-v0_8-whitegrid')

# Load the data
file_path = '/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv'
df = pd.read_csv(file_path)

# Convert periods to datetime for better plotting
df['Date'] = pd.to_datetime(df['Periods'], format='%Y %B', errors='coerce')

# Group by date and calculate mean turnover values for each month
monthly_data = df.groupby('Date').agg({
    'DomesticTurnover_5': 'mean',
    'ForeignTurnover_6': 'mean'
}).reset_index()

# Sort by date
monthly_data = monthly_data.sort_values('Date')

# Calculate 12-month moving averages to show trends more clearly
monthly_data['Domestic_MA'] = monthly_data['DomesticTurnover_5'].rolling(window=12).mean()
monthly_data['Foreign_MA'] = monthly_data['ForeignTurnover_6'].rolling(window=12).mean()

# Calculate the ratio of foreign to domestic turnover
monthly_data['Foreign_to_Domestic_Ratio'] = monthly_data['ForeignTurnover_6'] / monthly_data['DomesticTurnover_5']

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})

# Plot 1: Domestic vs Foreign Turnover
ax1.plot(monthly_data['Date'], monthly_data['DomesticTurnover_5'], 
       label='Domestic Turnover', linewidth=1, color='#1f77b4', alpha=0.7)
ax1.plot(monthly_data['Date'], monthly_data['ForeignTurnover_6'], 
       label='Foreign Turnover', linewidth=1, color='#ff7f0e', alpha=0.7)

# Add moving averages
ax1.plot(monthly_data['Date'], monthly_data['Domestic_MA'], 
       label='Domestic (12-month MA)', linewidth=2.5, color='#1f77b4')
ax1.plot(monthly_data['Date'], monthly_data['Foreign_MA'], 
       label='Foreign (12-month MA)', linewidth=2.5, color='#ff7f0e')

# Add recession periods (2008-2009 financial crisis and 2020 COVID-19)
ax1.axvspan(pd.Timestamp('2008-01-01'), pd.Timestamp('2009-06-30'), alpha=0.2, color='gray', label='2008-09 Financial Crisis')
ax1.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2020-12-31'), alpha=0.2, color='gray', label='COVID-19 Pandemic')

# Format the x-axis to show years
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax1.xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years

# Add labels and title for the first subplot
ax1.set_xlabel('')  # No label needed as it's shared with the second subplot
ax1.set_ylabel('Turnover Index (Average across all sectors)', fontsize=12)
ax1.set_title('Comparison of Domestic vs Foreign Turnover\nAverage across All Industry Sectors (2005-2023)', 
            fontsize=16, fontweight='bold')

# Add legend with a better position
ax1.legend(loc='upper left', fontsize=10, framealpha=0.9)

# Add grid for better readability
ax1.grid(True, alpha=0.3)

# Plot 2: Ratio of Foreign to Domestic Turnover
ax2.plot(monthly_data['Date'], monthly_data['Foreign_to_Domestic_Ratio'], 
       linewidth=1.5, color='#2ca02c', label='Monthly Ratio')

# Add moving average for the ratio
ax2.plot(monthly_data['Date'], monthly_data['Foreign_to_Domestic_Ratio'].rolling(window=12).mean(), 
       linewidth=2.5, color='#2ca02c', label='12-month MA', alpha=0.8)

# Add a horizontal line at ratio = 1 (equal domestic and foreign turnover)
ax2.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Equal Turnover')

# Format the x-axis to show years
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax2.xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years

# Add the same recession periods to the second subplot
ax2.axvspan(pd.Timestamp('2008-01-01'), pd.Timestamp('2009-06-30'), alpha=0.2, color='gray')
ax2.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2020-12-31'), alpha=0.2, color='gray')

# Add labels for the second subplot
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('Foreign/Domestic Ratio', fontsize=12)
ax2.set_title('Ratio of Foreign to Domestic Turnover', fontsize=14)

# Format the y-axis as percentage
ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2f}'.format(y)))

# Add legend
ax2.legend(loc='upper left', fontsize=10)

# Add grid for better readability
ax2.grid(True, alpha=0.3)

# Rotate x-axis labels for better readability
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)

# Add annotations for key events
# Financial crisis impact
ax1.annotate('Financial Crisis Impact', 
           xy=(pd.Timestamp('2009-01-01'), 85), 
           xytext=(pd.Timestamp('2009-03-01'), 70),
           arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
           fontsize=10)

# COVID-19 impact
ax1.annotate('COVID-19 Impact', 
           xy=(pd.Timestamp('2020-04-01'), 90), 
           xytext=(pd.Timestamp('2020-06-01'), 75),
           arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
           fontsize=10)

# Post-COVID recovery
ax1.annotate('Post-COVID Recovery', 
           xy=(pd.Timestamp('2021-06-01'), 150), 
           xytext=(pd.Timestamp('2021-09-01'), 165),
           arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
           fontsize=10)

# Tight layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_163933_industry_production_medium/visualization.png', dpi=300)

print("Plot saved successfully!")