# Automatically saved code from agent execution
# Run ID: 20250403_171545_municipal_accounts_medium, Iteration: 5

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set the style for the plot
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/municipal_accounts.csv')

# Let's examine what balance sheet items are available
balance_sheet_items = df['BalanceSheetItemsMunicipalities'].unique()

# For this visualization, we'll focus on "Total assets" if available, or "A - Assets" as a fallback
target_item = "Total assets" if "Total assets" in balance_sheet_items else "A - Assets"

# Filter for Zuid-Nederland (LD) region and the selected balance sheet item
filtered_df = df[(df['Regions'] == 'Zuid-Nederland (LD)') & 
                (df['BalanceSheetItemsMunicipalities'] == target_item)]

# Convert Periods to numeric to ensure proper sorting
filtered_df['Periods'] = pd.to_numeric(filtered_df['Periods'])

# Sort by period to ensure chronological order
filtered_df = filtered_df.sort_values('Periods')

# Get the current year
current_year = datetime.now().year

# Get the last 10 years of data
last_10_years = filtered_df.nlargest(10, 'Periods')

# Create the plot
plt.figure(figsize=(12, 7))

# Plot the trend line
sns.lineplot(
    data=last_10_years,
    x='Periods',
    y='BalanceSheetYearEndInEuroInhabit_2',
    marker='o',
    markersize=10,
    linewidth=2.5,
    color='#1f77b4'
)

# Add data points with values
for x, y in zip(last_10_years['Periods'], last_10_years['BalanceSheetYearEndInEuroInhabit_2']):
    plt.text(x, y + (max(last_10_years['BalanceSheetYearEndInEuroInhabit_2']) * 0.02), 
             f'€{y:,.0f}', ha='center', fontsize=10, fontweight='bold')

# Set title and labels
plt.title(f'Trend of Euros per Inhabitant for {target_item}\nin Zuid-Nederland (LD) Region (Last 10 Years)', 
          fontsize=16, pad=20)
plt.xlabel('Year', fontsize=14, labelpad=10)
plt.ylabel('Euros per Inhabitant (€)', fontsize=14, labelpad=10)

# Format the y-axis with euro symbol
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'€{x:,.0f}'))

# Adjust x-axis to show all years
plt.xticks(last_10_years['Periods'], rotation=0, fontsize=12)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Set y-axis to start from 0 for better perspective
plt.ylim(bottom=0)

# Add a note about the data source
plt.figtext(0.5, 0.01, 'Source: Municipal Accounts Data', 
            ha='center', fontsize=10, style='italic')

# Add a subtle background color to enhance readability
plt.gca().set_facecolor('#f8f9fa')

# Add a light border around the plot
for spine in plt.gca().spines.values():
    spine.set_edgecolor('#dddddd')
    spine.set_linewidth(0.8)

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_171545_municipal_accounts_medium/visualization.png', 
            dpi=300, bbox_inches='tight')

# Close the plot to free memory
plt.close()