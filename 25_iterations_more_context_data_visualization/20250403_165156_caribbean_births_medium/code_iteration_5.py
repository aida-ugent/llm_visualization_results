# Automatically saved code from agent execution
# Run ID: 20250403_165156_caribbean_births_medium, Iteration: 5

import pandas as pd

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/caribbean_births.csv')

# Check unique values in the CaribbeanNetherlands column
unique_regions = df['CaribbeanNetherlands'].unique()
print("Unique regions in the dataset:")
print(unique_regions)

# Print the first few rows for each unique region
for region in unique_regions:
    print(f"\nSample data for {region}:")
    print(df[df['CaribbeanNetherlands'] == region].head(2))