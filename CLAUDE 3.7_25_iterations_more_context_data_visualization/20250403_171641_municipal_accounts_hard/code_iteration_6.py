# Automatically saved code from agent execution
# Run ID: 20250403_171641_municipal_accounts_hard, Iteration: 6

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
pivot_df = filtered_df.pivot_table(
    index=['Regions', 'Periods'],
    columns='BalanceSheetItemsMunicipalities',
    values='BalanceSheetItemsYearEndInMlnEuro_1'
).reset_index()

# Create a more readable region name mapping
region_names = {
    'Noord-Nederland (LD)': 'North Netherlands',
    'Oost-Nederland (LD)': 'East Netherlands',
    'West-Nederland (LD)': 'West Netherlands',
    'Zuid-Nederland (LD)': 'South Netherlands'
}

# Apply the mapping
pivot_df['Region'] = pivot_df['Regions'].map(region_names)

# Set up the figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(18, 10))
fig.suptitle('Distribution of Fixed Assets by Region (2015-2022)', fontsize=18, y=0.98)

# Color palette for regions - using a colorblind-friendly palette
colors = sns.color_palette("colorblind", len(target_regions))
region_color_map = dict(zip(region_names.values(), colors))

# Plot for A12a - Other tangible fixed assets
ax1 = axes[0]
for region in region_names.values():
    region_data = pivot_df[pivot_df['Region'] == region]
    ax1.plot(
        region_data['Periods'], 
        region_data['A12a - Other tangible fixed assets'], 
        marker='o', 
        linewidth=2.5,
        markersize=8,
        label=region,
        color=region_color_map[region]
    )
ax1.set_title('Other Tangible Fixed Assets', fontsize=16)
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Value (Million Euros)', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(title='Region', loc='upper left', fontsize=12)
ax1.tick_params(axis='both', which='major', labelsize=12)

# Plot for A13 - Financial fixed assets
ax2 = axes[1]
for region in region_names.values():
    region_data = pivot_df[pivot_df['Region'] == region]
    ax2.plot(
        region_data['Periods'], 
        region_data['A13 - Financial fixed assets'], 
        marker='o', 
        linewidth=2.5,
        markersize=8,
        label=region,
        color=region_color_map[region]
    )
ax2.set_title('Financial Fixed Assets', fontsize=16)
ax2.set_xlabel('Year', fontsize=14)
ax2.set_ylabel('Value (Million Euros)', fontsize=14)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(title='Region', loc='upper left', fontsize=12)
ax2.tick_params(axis='both', which='major', labelsize=12)

# Set x-axis to show all years
for ax in axes:
    ax.set_xticks(target_years)
    ax.set_xticklabels(target_years, rotation=45)

# Add annotations for key trends
# West Netherlands has the highest values and notable changes
west_data = pivot_df[pivot_df['Region'] == 'West Netherlands']
max_tangible = west_data['A12a - Other tangible fixed assets'].max()
max_tangible_year = west_data.loc[west_data['A12a - Other tangible fixed assets'].idxmax(), 'Periods']
max_financial = west_data['A13 - Financial fixed assets'].max()
max_financial_year = west_data.loc[west_data['A13 - Financial fixed assets'].idxmax(), 'Periods']

# Annotate maximum points
ax1.annotate(f'Peak: {int(max_tangible)} M€', 
             xy=(max_tangible_year, max_tangible),
             xytext=(max_tangible_year-1, max_tangible+200),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=11)

ax2.annotate(f'Peak: {int(max_financial)} M€', 
             xy=(max_financial_year, max_financial),
             xytext=(max_financial_year-1, max_financial+300),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=11)

# Add a note about the significant drop in West Netherlands financial assets
financial_drop = west_data['A13 - Financial fixed assets'].iloc[0] - west_data['A13 - Financial fixed assets'].iloc[-1]
ax2.annotate(f'Drop: {int(financial_drop)} M€\n(2015-2022)', 
             xy=(2022, west_data['A13 - Financial fixed assets'].iloc[-1]),
             xytext=(2020, west_data['A13 - Financial fixed assets'].iloc[-1]-700),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=11)

# Add a descriptive text box with key insights
textstr = '\n'.join((
    'Key Insights:',
    '• West Netherlands has significantly higher asset values',
    '• Financial fixed assets show a declining trend across all regions',
    '• Other tangible fixed assets remain relatively stable',
    '• West Netherlands saw a major drop in financial assets (2015-2019)'
))
props = dict(boxstyle='round', facecolor='white', alpha=0.7)
fig.text(0.5, 0.02, textstr, fontsize=12, bbox=props, ha='center')

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.92, bottom=0.15)

# Save the figure
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_171641_municipal_accounts_hard/visualization.png', dpi=300, bbox_inches='tight')