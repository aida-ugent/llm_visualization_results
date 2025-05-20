# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Check the shape of the dataset
print(f"Dataset shape: {df.shape}")

# Check if there are any rows with Age not equal to 'Total'
non_total_age = df[df['Age'] != 'Total']
print(f"\nNumber of rows with Age not equal to 'Total': {len(non_total_age)}")

# Let's check if there are any rows with specific age values
if len(non_total_age) > 0:
    print("\nSample rows with specific age values:")
    print(non_total_age.head())
else:
    print("\nNo rows found with specific age values.")

# Let's check if there are any rows with specific marital status values
non_total_marital = df[df['MaritalStatus'] != 'Total']
print(f"\nNumber of rows with MaritalStatus not equal to 'Total': {len(non_total_marital)}")

# Let's check if there are any rows with specific migration background values
non_total_migration = df[df['MigrationBackground'] != 'Total']
print(f"\nNumber of rows with MigrationBackground not equal to 'Total': {len(non_total_migration)}")

# Let's check if there are rows with both specific marital status and migration background
specific_rows = df[(df['MaritalStatus'] != 'Total') & (df['MigrationBackground'] != 'Total')]
print(f"\nNumber of rows with both specific MaritalStatus and MigrationBackground: {len(specific_rows)}")

# Let's look at some of these rows if they exist
if len(specific_rows) > 0:
    print("\nSample rows with specific MaritalStatus and MigrationBackground:")
    print(specific_rows.head())

# Create a simple visualization to show the total population trend over time
plt.figure(figsize=(12, 7))
total_by_year = df[df['Age'] == 'Total'].groupby('Periods')['Population_1'].sum()
plt.plot(total_by_year.index, total_by_year.values, marker='o', linewidth=2)
plt.title('Total Population Trend in The Netherlands (1996-2022)', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Population', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png', dpi=300)