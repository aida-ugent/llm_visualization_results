# Automatically saved code from agent execution
# Run ID: 20250403_172703_population_medium, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the plot
sns.set_style("whitegrid")
plt.figure(figsize=(12, 8))

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for the years 2000 to 2010
df_filtered = df[(df['Periods'] >= 2000) & (df['Periods'] <= 2010)]

# Filter for specific marital statuses and sexes
# We need to check what values are available for MaritalStatus and Sex
print("Available MaritalStatus values:", df['MaritalStatus'].unique())
print("Available Sex values:", df['Sex'].unique())

# Check if we have Age = 'Total' for all combinations
print("\nChecking data availability:")
for sex in ['Males', 'Females']:
    for status in ['Never married', 'Married']:
        count = len(df_filtered[(df_filtered['Sex'] == sex) & 
                               (df_filtered['MaritalStatus'] == status) & 
                               (df_filtered['Age'] == 'Total')])
        print(f"Sex: {sex}, MaritalStatus: {status}, Count: {count}")