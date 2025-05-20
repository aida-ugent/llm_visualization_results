# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 10

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Get the most recent year
most_recent_year = df['Periods'].max()

# Filter for the most recent year and total age
df_recent = df[(df['Periods'] == most_recent_year) & (df['Age'] == 'Total')]

# Filter out rows where MigrationBackground is 'Total'
df_migration = df_recent[df_recent['MigrationBackground'] != 'Total']

# Group by MaritalStatus and MigrationBackground
# Since we found that MaritalStatus only has 'Total', we'll focus on MigrationBackground
migration_counts = df_migration.groupby('MigrationBackground')['Population_1'].sum().sort_values(ascending=False)

# Filter to include only the main migration background categories
main_categories = ['Dutch background', 'Western migration background', 'Non-western migration background']
other_categories = ['Africa', 'America', 'Asia', 'Europe (excluding Dutch background)', 'Oceania']
selected_categories = main_categories + other_categories

# Filter the data to include only these categories
migration_counts_filtered = migration_counts[migration_counts.index.isin(selected_categories)]

# Create a colorful bar chart
plt.figure(figsize=(14, 8))
colors = sns.color_palette('viridis', len(migration_counts_filtered))
bars = plt.bar(migration_counts_filtered.index, migration_counts_filtered.values, color=colors)

# Add data labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 5000,
             f'{height:,.0f}',
             ha='center', va='bottom', rotation=0, fontsize=9)

# Customize the plot
plt.title(f'Population Distribution by Migration Background in The Netherlands ({most_recent_year})', 
          fontsize=16, pad=20)
plt.xlabel('Migration Background', fontsize=14)
plt.ylabel('Population', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Format y-axis with commas
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))

# Add a note about the age limitation
plt.figtext(0.5, 0.01, 
            "Note: The dataset does not contain specific age groups like '75 to 80 years'. This visualization shows total population across all ages.", 
            ha='center', fontsize=10, style='italic')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png', 
            dpi=300, bbox_inches='tight')