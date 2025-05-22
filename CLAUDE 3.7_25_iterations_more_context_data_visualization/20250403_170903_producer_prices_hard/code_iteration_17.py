# Automatically saved code from agent execution
# Run ID: 20250403_170903_producer_prices_hard, Iteration: 17

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/ppi.csv')

# Extract year from the 'Periods' column
df['Year'] = df['Periods'].str.extract(r'(\d{4})').astype(int)

# Focus on 'Total sales' to get a consistent view across product categories
df_filtered = df[df['OutputAndImportPrices'] == 'Total sales']

# Manually select a diverse set of product categories
selected_categories = [
    'B Mining and quarrying',
    'C Manufactured products',
    '05 Coal and lignite',
    '06 Crude petroleum, natural gas...',
    '08 Other mining and quarrying p...',
    '081 Stone, sand and clay',
    '10 Food products',
    '105 Dairy products',
    '11 Beverages',
    '13 Textiles',
    '16 Wood and products of wood an...',
    '17 Paper and paper products',
    '19 Coke and refined petroleum p...',
    '20 Chemicals and chemical produ...',
    '22 Rubber and plastic products',
    '23 Other non-metallic mineral p...',
    '24 Basic metals',
    '25 Fabricated metal products, e...',
    '26 Computer, electronic and opt...',
    '27 Electrical equipment',
    '28 Machinery and equipment n.e.c.',
    '29 Motor vehicles, trailers and...',
    '31 Furniture',
    '35 Electricity, gas, steam and ...'
]

# Check which of these categories actually exist in the data
existing_categories = [cat for cat in selected_categories if cat in df_filtered['ProductsAccordingToPRODCOMList'].unique()]

# Calculate yearly averages for each selected product category
yearly_avg = df_filtered[df_filtered['ProductsAccordingToPRODCOMList'].isin(existing_categories)]
yearly_avg = yearly_avg.groupby(['ProductsAccordingToPRODCOMList', 'Year'])['PriceIndexNumbersExcludingExcise_1'].mean().reset_index()

# Create a pivot table for the heatmap
pivot_data = yearly_avg.pivot_table(
    values='PriceIndexNumbersExcludingExcise_1',
    index='ProductsAccordingToPRODCOMList',
    columns='Year'
)

# Create a figure with appropriate size
plt.figure(figsize=(16, 14))

# Create the heatmap
ax = sns.heatmap(
    pivot_data,
    annot=True,  # Show the values
    fmt='.1f',   # Format to 1 decimal place
    cmap='YlOrRd',  # Yellow-Orange-Red color map
    linewidths=0.5,
    cbar_kws={'label': 'Price Index (2015=100)'}
)

# Customize the plot
plt.title('Producer Price Index by Product Category and Year (2015=100)', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Product Category', fontsize=12)

# Rotate y-axis labels for better readability
plt.xticks(rotation=0)
plt.yticks(rotation=0)

# Add a note about the data
plt.figtext(0.5, 0.01, 'Note: Values represent yearly averages of monthly price indices (2015=100)', 
            ha='center', fontsize=10, style='italic')

# Highlight the reference year (2015)
for i, year in enumerate(pivot_data.columns):
    if year == 2015:
        plt.axvline(x=i+0.5, color='blue', linestyle='--', alpha=0.5)
        break

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170903_producer_prices_hard/visualization.png', dpi=300, bbox_inches='tight')