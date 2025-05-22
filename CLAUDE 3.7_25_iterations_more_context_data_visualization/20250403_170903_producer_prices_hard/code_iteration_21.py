# Automatically saved code from agent execution
# Run ID: 20250403_170903_producer_prices_hard, Iteration: 21

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
    if re.match(r'^\d{3}\s', category) and len(category.split(' ')[0]) == 3:
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

# Calculate the percentage change from 2015 to 2023
if 2015 in pivot_data.columns and 2023 in pivot_data.columns:
    pct_change = ((pivot_data[2023] - pivot_data[2015]) / pivot_data[2015] * 100).round(1)
    # Add this as a new column to the pivot table
    pivot_data['% Change\n2015-2023'] = pct_change

# Create a figure with appropriate size
plt.figure(figsize=(18, 20))

# Create the heatmap for the main data
ax = sns.heatmap(
    pivot_data.iloc[:, :-1] if '% Change\n2015-2023' in pivot_data.columns else pivot_data,  # Exclude the percentage change column
    annot=True,  # Show the values
    fmt='.1f',   # Format to 1 decimal place
    cmap='YlOrRd',  # Yellow-Orange-Red color map
    linewidths=0.5,
    cbar_kws={'label': 'Price Index (2015=100)'}
)

# If we have the percentage change column, add it as a separate heatmap
if '% Change\n2015-2023' in pivot_data.columns:
    # Create a separate colormap for the percentage change
    cmap_pct = sns.diverging_palette(10, 133, as_cmap=True)  # Blue-Red diverging palette
    
    # Get the position for the new column
    pos = ax.get_position()
    fig = plt.gcf()
    
    # Create a new axis for the percentage change column
    ax2 = fig.add_axes([pos.x1 + 0.01, pos.y0, 0.05, pos.height])
    
    # Create a heatmap for the percentage change
    sns.heatmap(
        pivot_data[['% Change\n2015-2023']],
        annot=True,
        fmt='.1f',
        cmap=cmap_pct,
        linewidths=0.5,
        cbar=False,
        ax=ax2,
        center=0  # Center the colormap at 0
    )
    
    # Add a title to the percentage change column
    ax2.set_title('% Change\n2015-2023', fontsize=10)
    ax2.set_xlabel('')
    ax2.set_yticks([])

# Customize the plot
plt.suptitle('Producer Price Index by Product Category and Year (2015=100)', fontsize=16, y=0.92)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Product Category', fontsize=12)

# Rotate y-axis labels for better readability
plt.xticks(rotation=0)
plt.yticks(rotation=0, fontsize=9)  # Smaller font for y-axis labels due to many categories

# Highlight the reference year (2015)
for i, year in enumerate(pivot_data.columns):
    if year == 2015:
        plt.axvline(x=i+0.5, color='blue', linestyle='--', alpha=0.5)
        break

# Add a note about the data
plt.figtext(0.5, 0.01, 'Note: Values represent yearly averages of monthly price indices (2015=100)', 
            ha='center', fontsize=10, style='italic')

# Adjust layout
plt.tight_layout(rect=[0, 0.02, 1, 0.95])  # Make room for the title and note

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170903_producer_prices_hard/visualization.png', dpi=300, bbox_inches='tight')