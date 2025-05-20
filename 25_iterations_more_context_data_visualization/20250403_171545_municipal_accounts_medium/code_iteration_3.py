# Automatically saved code from agent execution
# Run ID: 20250403_171545_municipal_accounts_medium, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set the style for the plot
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/municipal_accounts.csv')

# Filter for Zuid-Nederland (LD) region
zuid_nederland = df[df['Regions'] == 'Zuid-Nederland (LD)']

# Convert Periods to numeric to ensure proper sorting
zuid_nederland['Periods'] = pd.to_numeric(zuid_nederland['Periods'])

# Sort by period to ensure chronological order
zuid_nederland = zuid_nederland.sort_values('Periods')

# Get the current year
current_year = datetime.now().year

# Get the last 10 years of data
last_10_years = zuid_nederland[zuid_nederland['Periods'] >= current_year - 10]

# If we don't have enough data with that approach, let's take the 10 most recent years available
if len(last_10_years) < 5:  # If we have very few recent records
    last_10_years = zuid_nederland.nlargest(10, 'Periods')

# Create the plot
plt.figure(figsize=(12, 7))

# Plot the trend line
sns.lineplot(
    data=last_10_years,
    x='Periods',
    y='BalanceSheetYearEndInEuroInhabit_2',
    marker='o',
    markersize=8,
    linewidth=2
)

# Add data points
for x, y in zip(last_10_years['Periods'], last_10_years['BalanceSheetYearEndInEuroInhabit_2']):
    plt.text(x, y + 50, f'€{y:,.0f}', ha='center', fontsize=9)

# Set title and labels
plt.title('Trend of Euros per Inhabitant in Zuid-Nederland (LD) Region\nOver the Last 10 Years', 
          fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12, labelpad=10)
plt.ylabel('Euros per Inhabitant (€)', fontsize=12, labelpad=10)

# Format the y-axis with euro symbol
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'€{x:,.0f}'))

# Adjust x-axis to show all years
plt.xticks(last_10_years['Periods'], rotation=45)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add a note about the data source
plt.figtext(0.5, 0.01, 'Source: Municipal Accounts Data', 
            ha='center', fontsize=10, style='italic')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_171545_municipal_accounts_medium/visualization.png', 
            dpi=300, bbox_inches='tight')

# Close the plot to free memory
plt.close()