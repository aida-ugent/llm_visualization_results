# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 12

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Check unique values in MaritalStatus column
marital_statuses = df['MaritalStatus'].unique()
print("Unique MaritalStatus values:")
print(marital_statuses)

# Check if there are any rows with MaritalStatus not equal to 'Total'
non_total_marital = df[df['MaritalStatus'] != 'Total']
print(f"\nNumber of rows with MaritalStatus not equal to 'Total': {len(non_total_marital)}")

# Let's check if there are any rows with Age not equal to 'Total' in the entire dataset
non_total_age = df[df['Age'] != 'Total']
print(f"\nNumber of rows with Age not equal to 'Total': {len(non_total_age)}")

# Let's check the unique values in the Sex column
print("\nUnique Sex values:")
print(df['Sex'].unique())

# Let's check if there are any rows with Sex not equal to 'Total males and females'
non_total_sex = df[df['Sex'] != 'Total males and females']
print(f"\nNumber of rows with Sex not equal to 'Total males and females': {len(non_total_sex)}")

# Let's check if there are any rows with specific values in multiple columns
specific_rows = df[(df['Sex'] != 'Total males and females') | 
                   (df['Age'] != 'Total') | 
                   (df['MaritalStatus'] != 'Total')]
print(f"\nNumber of rows with specific values in Sex, Age, or MaritalStatus: {len(specific_rows)}")

# If there are specific rows, let's look at a sample
if len(specific_rows) > 0:
    print("\nSample of rows with specific values:")
    print(specific_rows.head())

# Create a simple visualization to show the distribution by migration background for the most recent year
most_recent_year = df['Periods'].max()
df_recent = df[(df['Periods'] == most_recent_year)]

# Create a pie chart of the main migration background categories
main_categories = ['Dutch background', 'Western migration background', 'Non-western migration background']
df_main = df_recent[df_recent['MigrationBackground'].isin(main_categories)]
migration_counts = df_main.groupby('MigrationBackground')['Population_1'].sum()

plt.figure(figsize=(12, 8))
colors = sns.color_palette('viridis', len(migration_counts))
plt.pie(migration_counts, labels=migration_counts.index, autopct='%1.1f%%', 
        startangle=90, colors=colors, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
plt.title(f'Population Distribution by Main Migration Background Categories ({most_recent_year})', fontsize=16)

# Add a note about the age limitation
plt.figtext(0.5, 0.01, 
            "Note: The dataset does not contain specific age groups like '75 to 80 years' or specific marital status categories.\nThis visualization shows total population across all ages and marital statuses.", 
            ha='center', fontsize=10, style='italic')

plt.tight_layout()
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png', 
            dpi=300, bbox_inches='tight')