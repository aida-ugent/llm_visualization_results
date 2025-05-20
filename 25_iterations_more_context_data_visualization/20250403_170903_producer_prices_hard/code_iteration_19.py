# Automatically saved code from agent execution
# Run ID: 20250403_170903_producer_prices_hard, Iteration: 19

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

# Get unique product categories
unique_products = df_filtered['ProductsAccordingToPRODCOMList'].unique()

# Define a function to identify main categories and important subcategories
def is_main_or_important_category(category):
    # Main categories (B, C)
    if category.startswith('B ') or category.startswith('C '):
        return True
    
    # Important two-digit categories (like 10, 19, 24)
    if re.match(r'^\d{2}\s', category):
        return True
    
    # Important three-digit subcategories (like 105, 235)
    if re.match(r'^\d{3}\s', category):
        return True
    
    return False

# Filter categories
selected_categories = [cat for cat in unique_products if is_main_or_important_category(cat)]

# Calculate yearly averages for each selected product category
yearly_avg = df_filtered[df_filtered['ProductsAccordingToPRODCOMList'].isin(selected_categories)]
yearly_avg = yearly_avg.groupby(['ProductsAccordingToPRODCOMList', 'Year'])['PriceIndexNumbersExcludingExcise_1'].mean().reset_index()

# Create a pivot table for the heatmap
pivot_data = yearly_avg.pivot_table(
    values='PriceIndexNumbersExcludingExcise_1',
    index='ProductsAccordingToPRODCOMList',
    columns='Year'
)

# Sort the index to have a more logical order
# First, separate categories by their prefix type
main_cats = [cat for cat in pivot_data.index if cat.startswith(('B ', 'C '))]
two_digit_cats = [cat for cat in pivot_data.index if re.match(r'^\d{2}\s', cat)]
three_digit_cats = [cat for cat in pivot_data.index if re.match(r'^\d{3}\s', cat)]

# Sort each group
main_cats.sort()
two_digit_cats.sort()
three_digit_cats.sort()

# Combine them in a logical order
sorted_categories = main_cats + two_digit_cats + three_digit_cats
pivot_data = pivot_data.reindex(sorted_categories)

# Create a figure with appropriate size
plt.figure(figsize=(16, 20))

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
plt.yticks(rotation=0, fontsize=9)  # Smaller font for y-axis labels due to many categories

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