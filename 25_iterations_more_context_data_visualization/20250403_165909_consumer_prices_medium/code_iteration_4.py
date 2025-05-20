# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 4

import pandas as pd

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Print the first few unique expenditure categories
unique_categories = df['ExpenditureCategories'].unique()
print(f"Number of unique categories: {len(unique_categories)}")
print("First 20 unique categories:")
for i, category in enumerate(unique_categories[:20]):
    print(f"{i+1}. {category}")