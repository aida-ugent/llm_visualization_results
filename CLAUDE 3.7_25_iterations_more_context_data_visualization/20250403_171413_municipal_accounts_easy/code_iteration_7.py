# Automatically saved code from agent execution
# Run ID: 20250403_171413_municipal_accounts_easy, Iteration: 7

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style
sns.set_style("whitegrid")

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

# Create a figure with two subplots - one for all items and one for smaller items
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1]})

# Plot all items in the first subplot
pivot_df.plot(kind='line', marker='o', linewidth=2.5, markersize=6, ax=ax1)
ax1.set_title('Balance Sheet Items Year-End Values Over Time in the Netherlands', fontsize=16, pad=20)
ax1.set_xlabel('')  # No x-label for the top plot
ax1.set_ylabel('Value (Million Euro)', fontsize=14)
ax1.grid(True, alpha=0.3)
ax1.legend(title='Balance Sheet Items', title_fontsize=12, fontsize=10, 
          bbox_to_anchor=(1.05, 1), loc='upper left')

# Plot only the smaller items in the second subplot for better visibility
smaller_items = ['A11 - Intangible assets', 'A13 - Financial fixed assets']
pivot_df[smaller_items].plot(kind='line', marker='o', linewidth=2.5, markersize=6, ax=ax2)
ax2.set_title('Focus on Smaller Balance Sheet Items', fontsize=14, pad=15)
ax2.set_xlabel('Year', fontsize=14)
ax2.set_ylabel('Value (Million Euro)', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.legend(title='Balance Sheet Items', title_fontsize=12, fontsize=10,
          bbox_to_anchor=(1.05, 1), loc='upper left')

# Rotate x-axis labels for better readability
for ax in [ax1, ax2]:
    ax.tick_params(axis='x', rotation=45)

# Add annotations for key trends
# Find the last values for each category
last_year = pivot_df.index.max()
for category in main_categories:
    last_value = pivot_df.loc[last_year, category]
    if category == 'A - Assets':
        ax1.annotate(f"{int(last_value)} M€", 
                    xy=(last_year, last_value),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=10, fontweight='bold')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_171413_municipal_accounts_easy/visualization.png', 
            dpi=300, bbox_inches='tight')