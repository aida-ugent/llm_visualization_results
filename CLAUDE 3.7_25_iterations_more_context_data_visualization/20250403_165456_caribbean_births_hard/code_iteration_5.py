# Automatically saved code from agent execution
# Run ID: 20250403_165456_caribbean_births_hard, Iteration: 5

import pandas as pd

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/caribbean_births.csv')

# Check unique values in CaribbeanNetherlands column
print("Unique values in CaribbeanNetherlands column:")
print(df['CaribbeanNetherlands'].unique())

# Check if we have data for 2015
print("\nYears available in the dataset:")
print(df['Periods'].unique())

# Check if we have data for Bonaire in 2015
bonaire_2015 = df[(df['CaribbeanNetherlands'] == 'Bonaire') & (df['Periods'] == 2015)]
print("\nNumber of records for Bonaire in 2015:", len(bonaire_2015))

if len(bonaire_2015) > 0:
    print("\nSample of Bonaire 2015 data:")
    print(bonaire_2015[['CaribbeanNetherlands', 'Periods', 'MotherMarried_22', 'MotherNeverMarried_23']].head())