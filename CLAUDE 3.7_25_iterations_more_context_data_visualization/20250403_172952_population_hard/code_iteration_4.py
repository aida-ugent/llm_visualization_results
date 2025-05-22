# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 4

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Check if '75 to 80 years' exists in the Age column
print("Age values containing '75':")
print(df['Age'].unique()[df['Age'].str.contains('75', na=False) if hasattr(df['Age'], 'str') else []])

# Let's check all unique age values to find the correct format
print("\nAll unique Age values:")
print(df['Age'].unique())

# Let's check the data types
print("\nData types:")
print(df.dtypes)

# Let's check if there are any records with age around 75-80 years
sample_data = df[df['Age'].astype(str).str.contains('75|80', na=False)].head(10)
print("\nSample data for ages containing '75' or '80':")
print(sample_data)

# Create a simple plot to test
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, "Data Exploration", ha='center', va='center', fontsize=20)
plt.axis('off')
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png')