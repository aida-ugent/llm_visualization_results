# Automatically saved code from agent execution
# Run ID: 20250403_172703_population_medium, Iteration: 5

import pandas as pd

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Check unique values for Sex and MaritalStatus
print("Unique values for Sex:")
print(df['Sex'].unique())
print("\nUnique values for MaritalStatus:")
print(df['MaritalStatus'].unique())

# Let's see if we can find rows with different MaritalStatus values
sample_rows = df[df['MaritalStatus'] != 'Total'].head(10)
print("\nSample rows with non-Total MaritalStatus:")
print(sample_rows[['Sex', 'Age', 'MaritalStatus', 'Periods', 'Population_1']])