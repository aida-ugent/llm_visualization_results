# Automatically saved code from agent execution
# Run ID: 20250403_171413_municipal_accounts_easy, Iteration: 9

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import FuncFormatter

# Set the style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/municipal_accounts.csv')

# Filter for Netherlands data and main balance sheet categories
main_categories = ['A - Assets', 'A1 - Fixed assets', 'A11 - Intangible assets', 
                  'A12 - Tangible fixed assets', 'A13 - Financial fixed assets']
filtered_df = df[(df['Regions'] == 'The Netherlands') & 
                (df['BalanceSheetItemsMunicipalities'].isin(main_categories))]

# Pivot the data for plotting
pivot_df = filtered_df.pivot(index='Periods', 
                            columns='BalanceSheetItemsMunicipalities', 
                            values='BalanceSheetItemsYearEndInMlnEuro_1')

# Calculate growth rates from 2004 to 2022
growth_rates = {}
for category in main_categories:
    start_value = pivot_df.loc[2004, category]
    end_value = pivot_df.loc[pivot_df.index.max(), category]
    growth_pct = ((end_value - start_value) / start_value) * 100
    growth_rates[category] = growth_pct

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1]})

# Color palette
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Plot all items in the first subplot
for i, category in enumerate(main_categories):
    ax1.plot(pivot_df.index, pivot_df[category], marker='o', linewidth=2.5, 
             markersize=6, label=category, color=colors[i])

# Format y-axis to show thousands separator
def billions_formatter(x, pos):
    return f'{x/1000:.1f}B' if x >= 1000 else f'{x:.0f}M'

ax1.yaxis.set_major_formatter(FuncFormatter(billions_formatter))

# Add titles and labels
ax1.set_title('Balance Sheet Items Year-End Values Over Time in the Netherlands', fontsize=16, pad=20)
ax1.set_xlabel('')  # No x-label for the top plot
ax1.set_ylabel('Value (Euro)', fontsize=14)
ax1.grid(True, alpha=0.3)
ax1.legend(title='Balance Sheet Items', title_fontsize=12, fontsize=10, 
          bbox_to_anchor=(1.05, 1), loc='upper left')

# Add annotations for the last values and growth rates
last_year = pivot_df.index.max()
for i, category in enumerate(main_categories):
    last_value = pivot_df.loc[last_year, category]
    growth = growth_rates[category]
    
    # Only annotate the main categories to avoid clutter
    if category in ['A - Assets', 'A1 - Fixed assets', 'A12 - Tangible fixed assets']:
        ax1.annotate(f"{int(last_value)} M€ ({growth:.1f}%)", 
                    xy=(last_year, last_value),
                    xytext=(10, 0), textcoords='offset points',
                    fontsize=9, fontweight='bold', color=colors[i])

# Plot only the smaller items in the second subplot for better visibility
smaller_items = ['A11 - Intangible assets', 'A13 - Financial fixed assets']
colors_small = [colors[2], colors[4]]  # Use the same colors as in the main plot

for i, category in enumerate(smaller_items):
    ax2.plot(pivot_df.index, pivot_df[category], marker='o', linewidth=2.5, 
             markersize=6, label=category, color=colors_small[i])

ax2.set_title('Focus on Smaller Balance Sheet Items', fontsize=14, pad=15)
ax2.set_xlabel('Year', fontsize=14)
ax2.set_ylabel('Value (Million Euro)', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.legend(title='Balance Sheet Items', title_fontsize=12, fontsize=10,
          bbox_to_anchor=(1.05, 1), loc='upper left')

# Add annotations for the smaller items
for i, category in enumerate(smaller_items):
    last_value = pivot_df.loc[last_year, category]
    growth = growth_rates[category]
    ax2.annotate(f"{int(last_value)} M€ ({growth:.1f}%)", 
                xy=(last_year, last_value),
                xytext=(10, 0), textcoords='offset points',
                fontsize=9, fontweight='bold', color=colors_small[i])

# Rotate x-axis labels for better readability
for ax in [ax1, ax2]:
    ax.tick_params(axis='x', rotation=45)

# Add a note about the data source
fig.text(0.5, 0.01, 'Source: Statistics Netherlands (CBS)', ha='center', fontsize=10, style='italic')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_171413_municipal_accounts_easy/visualization.png', 
            dpi=300, bbox_inches='tight')