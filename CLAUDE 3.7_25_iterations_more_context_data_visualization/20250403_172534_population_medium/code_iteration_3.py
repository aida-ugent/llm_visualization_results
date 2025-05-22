# Automatically saved code from agent execution
# Run ID: 20250403_172534_population_medium, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for the year 2010
df_2010 = df[df['Periods'] == 2010]

# Check unique values in MigrationBackground
migration_backgrounds = df_2010['MigrationBackground'].unique()
print("Unique Migration Backgrounds in 2010:")
print(migration_backgrounds)

# Check if we have data for total population by migration background
print("\nSample data for 2010 by migration background:")
sample = df_2010[(df_2010['Sex'] == 'Total males and females') & 
                (df_2010['Age'] == 'Total') & 
                (df_2010['MaritalStatus'] == 'Total') &
                (df_2010['Generation'] == 'Total')]
print(sample[['MigrationBackground', 'Population_1']].head(10))