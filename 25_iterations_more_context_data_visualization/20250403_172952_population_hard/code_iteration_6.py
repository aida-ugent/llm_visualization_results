# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 6

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Check the first few rows to understand the structure
print("First 5 rows:")
print(df.head())

# Check if there are more detailed age groups in the dataset
print("\nSample rows with different Age values:")
sample_ages = df[df['Age'] != 'Total'].head(10)
print(sample_ages)

# Check the unique values in the Age column
print("\nNumber of unique Age values:", df['Age'].nunique())
print("\nSample of unique Age values:")
print(df['Age'].unique()[:20])  # Show first 20 unique values

# Check the years available in the dataset
print("\nYears available in the dataset:")
print(sorted(df['Periods'].unique()))

# Let's create a simple visualization to check if we can plot
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, "Data Structure Analysis", ha='center', va='center', fontsize=20)
plt.axis('off')
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png')