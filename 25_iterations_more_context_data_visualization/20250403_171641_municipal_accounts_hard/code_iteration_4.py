# Automatically saved code from agent execution
# Run ID: 20250403_171641_municipal_accounts_hard, Iteration: 4

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/municipal_accounts.csv')

# Filter for the specific balance sheet items we're interested in
target_items = ['A12a - Other tangible fixed assets', 'A13 - Financial fixed assets']
target_regions = ['Noord-Nederland (LD)', 'Oost-Nederland (LD)', 'West-Nederland (LD)', 'Zuid-Nederland (LD)']
target_years = list(range(2015, 2023))  # 2015-2022

# Filter the dataframe
filtered_df = df[
    df['BalanceSheetItemsMunicipalities'].isin(target_items) & 
    df['Regions'].isin(target_regions) & 
    df['Periods'].isin(target_years)
]

# Pivot the data for easier plotting
# We'll use the values in millions of euros
pivot_df = filtered_df.pivot_table(
    index=['Regions', 'Periods'],
    columns='BalanceSheetItemsMunicipalities',
    values='BalanceSheetItemsYearEndInMlnEuro_1'
).reset_index()

# Set up the figure with subplots - one for each asset type
fig, axes = plt.subplots(2, 1, figsize=(14, 12), sharex=True)
fig.suptitle('Distribution of Fixed Assets by Region (2015-2022)', fontsize=16, y=0.95)

# Color palette for regions
colors = sns.color_palette("viridis", len(target_regions))
region_color_map = dict(zip(target_regions, colors))

# Plot for A12a - Other tangible fixed assets
ax1 = axes[0]
for region in target_regions:
    region_data = pivot_df[pivot_df['Regions'] == region]
    ax1.plot(
        region_data['Periods'], 
        region_data['A12a - Other tangible fixed assets'], 
        marker='o', 
        linewidth=2,
        label=region,
        color=region_color_map[region]
    )
ax1.set_title('A12a - Other tangible fixed assets', fontsize=14)
ax1.set_ylabel('Value (Million Euros)', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(title='Region', loc='upper left')

# Plot for A13 - Financial fixed assets
ax2 = axes[1]
for region in target_regions:
    region_data = pivot_df[pivot_df['Regions'] == region]
    ax2.plot(
        region_data['Periods'], 
        region_data['A13 - Financial fixed assets'], 
        marker='o', 
        linewidth=2,
        label=region,
        color=region_color_map[region]
    )
ax2.set_title('A13 - Financial fixed assets', fontsize=14)
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('Value (Million Euros)', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(title='Region', loc='upper left')

# Set x-axis to show all years
for ax in axes:
    ax.set_xticks(target_years)
    ax.set_xticklabels(target_years, rotation=45)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.92)

# Save the figure
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_171641_municipal_accounts_hard/visualization.png', dpi=300, bbox_inches='tight')