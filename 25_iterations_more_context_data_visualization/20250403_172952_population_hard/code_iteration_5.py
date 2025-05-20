# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 5

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Check unique age values
print("Unique Age values:")
age_values = df['Age'].unique()
for age in age_values[:20]:  # Print first 20 to avoid overwhelming output
    print(f"- {age}")

print(f"\nTotal unique age values: {len(age_values)}")

# Check if '75 to 80 years' exists
has_75_to_80 = '75 to 80 years' in age_values
print(f"\n'75 to 80 years' exists in the dataset: {has_75_to_80}")

# If not, find similar age ranges
if not has_75_to_80:
    similar_ages = [age for age in age_values if '75' in str(age) or '80' in str(age)]
    print("\nSimilar age ranges:")
    for age in similar_ages:
        print(f"- {age}")

# Check unique marital status values
print("\nUnique MaritalStatus values:")
for status in df['MaritalStatus'].unique():
    print(f"- {status}")

# Check unique migration background values
print("\nUnique MigrationBackground values:")
for background in df['MigrationBackground'].unique():
    print(f"- {background}")

# Create a simple plot to test
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, "Data Exploration", ha='center', va='center', fontsize=20)
plt.axis('off')
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png')