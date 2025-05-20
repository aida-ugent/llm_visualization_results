# Automatically saved code from agent execution
# Run ID: 20250403_170903_producer_prices_hard, Iteration: 13

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/ppi.csv')

# Extract year from the 'Periods' column
df['Year'] = df['Periods'].str.extract(r'(\d{4})').astype(int)

# Focus on 'Total sales' to get a consistent view across product categories
df_filtered = df[df['OutputAndImportPrices'] == 'Total sales']

# Calculate yearly averages for each product category
yearly_avg = df_filtered.groupby(['ProductsAccordingToPRODCOMList', 'Year'])['PriceIndexNumbersExcludingExcise_1'].mean().reset_index()

# Get a list of product categories that start with a single letter or a letter followed by a number
# These are typically the main categories
pattern = r'^[A-Z](\s|$)|^[A-Z][0-9]+'
main_categories = yearly_avg['ProductsAccordingToPRODCOMList'].unique()
main_categories = [cat for cat in main_categories if re.match(pattern, cat)]

# Filter to include only these main categories
yearly_avg_main = yearly_avg[yearly_avg['ProductsAccordingToPRODCOMList'].isin(main_categories)]

# Create a pivot table for the heatmap
pivot_data = yearly_avg_main.pivot_table(
    values='PriceIndexNumbersExcludingExcise_1',
    index='ProductsAccordingToPRODCOMList',
    columns='Year'
)

# Sort the categories for better visualization
# First, separate single-letter categories and two-digit categories
single_letter = [cat for cat in pivot_data.index if len(cat) < 3]
two_digit = [cat for cat in pivot_data.index if len(cat) >= 3]

# Sort them separately
single_letter.sort()
two_digit.sort()

# Combine them back
sorted_categories = single_letter + two_digit
pivot_data = pivot_data.reindex(sorted_categories)

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