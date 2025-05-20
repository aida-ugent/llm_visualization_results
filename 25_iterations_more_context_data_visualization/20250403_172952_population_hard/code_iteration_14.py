# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 14

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for main migration background categories
main_categories = ['Dutch background', 'Western migration background', 'Non-western migration background']
df_main = df[df['MigrationBackground'].isin(main_categories)]

# Group by year and migration background
migration_by_year = df_main.pivot_table(
    index='Periods', 
    columns='MigrationBackground', 
    values='Population_1', 
    aggfunc='sum'
)

# Create a stacked area chart
plt.figure(figsize=(14, 8))
plt.stackplot(migration_by_year.index, 
              migration_by_year['Dutch background'],
              migration_by_year['Western migration background'],
              migration_by_year['Non-western migration background'],
              labels=['Dutch background', 'Western migration background', 'Non-western migration background'],
              alpha=0.8)

# Add a line for the total population
total_by_year = df[df['MigrationBackground'] == 'Total'].groupby('Periods')['Population_1'].sum()
plt.plot(total_by_year.index, total_by_year.values, 'k--', label='Total Population', linewidth=2)

# Customize the plot
plt.title('Population Trends by Migration Background in The Netherlands (1996-2022)', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Population', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper left', fontsize=12)

# Format y-axis with commas
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))

# Add annotations for the most recent year
last_year = migration_by_year.index[-1]
dutch_last = migration_by_year['Dutch background'].iloc[-1]
western_last = migration_by_year['Western migration background'].iloc[-1]
non_western_last = migration_by_year['Non-western migration background'].iloc[-1]

plt.annotate(f'Dutch: {dutch_last:,.0f}', 
             xy=(last_year, dutch_last/2), 
             xytext=(last_year+0.5, dutch_last/2),
             fontsize=10, color='white', fontweight='bold')

plt.annotate(f'Western: {western_last:,.0f}', 
             xy=(last_year, dutch_last + western_last/2), 
             xytext=(last_year+0.5, dutch_last + western_last/2),
             fontsize=10, color='white', fontweight='bold')

plt.annotate(f'Non-western: {non_western_last:,.0f}', 
             xy=(last_year, dutch_last + western_last + non_western_last/2), 
             xytext=(last_year+0.5, dutch_last + western_last + non_western_last/2),
             fontsize=10, color='white', fontweight='bold')

# Add a note about the age limitation
plt.figtext(0.5, 0.01, 
            "Note: The dataset does not contain specific age groups like '75 to 80 years' or specific marital status categories.\nThis visualization shows total population across all ages and marital statuses.", 
            ha='center', fontsize=10, style='italic')

plt.tight_layout()
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png', 
            dpi=300, bbox_inches='tight')