# Automatically saved code from agent execution
# Run ID: 20250403_170903_producer_prices_hard, Iteration: 7

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/ppi.csv')

# Extract year from the 'Periods' column
df['Year'] = df['Periods'].str.extract(r'(\d{4})').astype(int)

# Get unique OutputAndImportPrices values to understand the data structure
output_types = df['OutputAndImportPrices'].unique()

# Focus on 'Total sales' to get a consistent view across product categories
df_filtered = df[df['OutputAndImportPrices'] == 'Total sales']

# Select main product categories (first level categories)
# We'll identify these by looking for patterns in the product names
main_categories = []
for cat in df_filtered['ProductsAccordingToPRODCOMList'].unique():
    # Check if it's a main category (typically starts with a letter followed by a space)
    if ' ' in cat and cat[0].isalpha() and not cat[1].isdigit():
        main_categories.append(cat)
    # Also include categories that start with a letter and a number (like C10)
    elif len(cat) >= 2 and cat[0].isalpha() and cat[1].isdigit():
        main_categories.append(cat)

# Filter to include only these main categories
df_main = df_filtered[df_filtered['ProductsAccordingToPRODCOMList'].isin(main_categories)]

# Create a pivot table for the heatmap
pivot_data = df_main.pivot_table(
    values='PriceIndexNumbersExcludingExcise_1',
    index='ProductsAccordingToPRODCOMList',
    columns='Year',
    aggfunc='mean'  # Using mean for yearly average
)

# Sort the index to have a more logical order
pivot_data = pivot_data.sort_index()

# Create a figure with appropriate size
plt.figure(figsize=(16, 12))

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
plt.title('Average Producer Price Index by Product Category and Year (2015=100)', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Product Category', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=0)
plt.yticks(rotation=0)

# Add a note about the data
plt.figtext(0.5, 0.01, 'Note: Values represent yearly averages of monthly price indices (2015=100)', 
            ha='center', fontsize=10, style='italic')

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170903_producer_prices_hard/visualization.png', dpi=300, bbox_inches='tight')