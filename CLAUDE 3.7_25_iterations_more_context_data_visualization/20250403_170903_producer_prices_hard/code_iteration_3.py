# Automatically saved code from agent execution
# Run ID: 20250403_170903_producer_prices_hard, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/ppi.csv')

# Extract year from the 'Periods' column
df['Year'] = df['Periods'].str.extract(r'(\d{4})').astype(int)

# Focus on the price index numbers
# Group by year and product categories
pivot_data = df.pivot_table(
    values='PriceIndexNumbersExcludingExcise_1',
    index='ProductsAccordingToPRODCOMList',
    columns='Year',
    aggfunc='mean'  # Using mean for yearly average
)

# Create a figure with appropriate size
plt.figure(figsize=(14, 10))

# Create the heatmap
ax = sns.heatmap(
    pivot_data,
    annot=False,  # Too many values to annotate
    cmap='YlOrRd',  # Yellow-Orange-Red color map (good for price indices)
    linewidths=0.5,
    cbar_kws={'label': 'Price Index (2015=100)'}
)

# Customize the plot
plt.title('Average Price Index by Product Category and Year (2015=100)', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Product Category', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=0)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170903_producer_prices_hard/visualization.png', dpi=300, bbox_inches='tight')