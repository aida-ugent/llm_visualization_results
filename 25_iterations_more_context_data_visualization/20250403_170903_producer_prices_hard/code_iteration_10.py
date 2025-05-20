# Automatically saved code from agent execution
# Run ID: 20250403_170903_producer_prices_hard, Iteration: 10

import pandas as pd

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/ppi.csv')

# Get unique product categories
unique_products = df['ProductsAccordingToPRODCOMList'].unique()

# Print the first 30 unique product categories to understand the structure
print("First 30 unique product categories:")
for i, product in enumerate(unique_products[:30]):
    print(f"{i+1}. {product}")

# Count total unique product categories
print(f"\nTotal unique product categories: {len(unique_products)}")

# Save this information to a text file (not a visualization)
with open('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170903_producer_prices_hard/product_categories.txt', 'w') as f:
    f.write("All unique product categories:\n")
    for i, product in enumerate(unique_products):
        f.write(f"{i+1}. {product}\n")