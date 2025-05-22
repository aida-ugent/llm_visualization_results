# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for the age group '75 to 80 years'
age_filter = df['Age'] == '75 to 80 years'
df_filtered = df[age_filter]

# Get the most recent year
most_recent_year = df_filtered['Periods'].max()
df_recent = df_filtered[df_filtered['Periods'] == most_recent_year]

# Filter out 'Total' values for MaritalStatus and MigrationBackground
df_recent = df_recent[(df_recent['MaritalStatus'] != 'Total') & 
                      (df_recent['MigrationBackground'] != 'Total')]

# Create a pivot table for visualization
pivot_df = df_recent.pivot_table(
    index='MaritalStatus',
    columns='MigrationBackground',
    values='Population_1',
    aggfunc='sum'
)

# Replace NaN with 0
pivot_df = pivot_df.fillna(0)

# Create the plot
plt.figure(figsize=(14, 8))
pivot_df.plot(kind='bar', ax=plt.gca())

# Customize the plot
plt.title(f'Distribution of 75-80 Year Olds by Marital Status and Migration Background ({most_recent_year})', 
          fontsize=16, pad=20)
plt.xlabel('Marital Status', fontsize=14)
plt.ylabel('Population', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Migration Background', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add commas to y-axis labels for better readability
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png', 
            dpi=300, bbox_inches='tight')

print(f"Most recent year in dataset: {most_recent_year}")
print(f"Unique marital statuses: {df_recent['MaritalStatus'].unique()}")
print(f"Unique migration backgrounds: {df_recent['MigrationBackground'].unique()}")