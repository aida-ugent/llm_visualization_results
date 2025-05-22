# Automatically saved code from agent execution
# Run ID: 20250403_172703_population_medium, Iteration: 6

import pandas as pd

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Check the shape of the dataset
print(f"Dataset shape: {df.shape}")

# Let's look at some random samples to see if there are more detailed breakdowns
print("\nRandom sample of 10 rows:")
random_sample = df.sample(10)
print(random_sample[['ID', 'Sex', 'Age', 'MaritalStatus', 'Generation', 'MigrationBackground', 'Periods', 'Population_1']])

# Let's check if there are any rows with Sex not equal to 'Total males and females'
non_total_sex = df[df['Sex'] != 'Total males and females'].head(5)
print("\nRows with Sex not 'Total males and females':")
print(non_total_sex[['ID', 'Sex', 'Age', 'MaritalStatus', 'Periods', 'Population_1']] if not non_total_sex.empty else "None found")

# Let's check if there are any rows with MaritalStatus not equal to 'Total'
non_total_marital = df[df['MaritalStatus'] != 'Total'].head(5)
print("\nRows with MaritalStatus not 'Total':")
print(non_total_marital[['ID', 'Sex', 'Age', 'MaritalStatus', 'Periods', 'Population_1']] if not non_total_marital.empty else "None found")