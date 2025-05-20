# Automatically saved code from agent execution
# Run ID: 20250403_172952_population_hard, Iteration: 16

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for main migration background categories and more detailed ones
main_categories = ['Dutch background', 'Western migration background', 'Non-western migration background']
detailed_categories = ['Africa', 'America', 'Asia', 'Europe (excluding Dutch background)']
selected_categories = main_categories + detailed_categories

df_selected = df[df['MigrationBackground'].isin(selected_categories)]

# Group by year and migration background
migration_by_year = df_selected.pivot_table(
    index='Periods', 
    columns='MigrationBackground', 
    values='Population_1', 
    aggfunc='sum'
)

# Create a line chart
plt.figure(figsize=(14, 10))

# Plot main categories with thicker lines
for category in main_categories:
    plt.plot(migration_by_year.index, migration_by_year[category], 
             linewidth=3, marker='o', markersize=6, 
             label=category)

# Plot detailed categories with thinner lines
for category in detailed_categories:
    if category in migration_by_year.columns:
        plt.plot(migration_by_year.index, migration_by_year[category], 
                 linewidth=1.5, marker='.', markersize=4, 
                 label=category, linestyle='--')

# Customize the plot
plt.title('Population Trends by Migration Background in The Netherlands (1996-2022)', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Population', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

# Format y-axis with commas
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))

# Add annotations for the most recent year
last_year = migration_by_year.index[-1]
for category in selected_categories:
    if category in migration_by_year.columns:
        last_value = migration_by_year[category].iloc[-1]
        plt.annotate(f'{last_value:,.0f}', 
                     xy=(last_year, last_value), 
                     xytext=(last_year+0.5, last_value),
                     fontsize=9, fontweight='bold')

# Add a note about the age limitation
plt.figtext(0.5, 0.01, 
            "Note: The dataset does not contain specific age groups like '75 to 80 years' or specific marital status categories.\nThis visualization shows total population across all ages and marital statuses.", 
            ha='center', fontsize=10, style='italic')

plt.tight_layout()
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172952_population_hard/visualization.png', 
            dpi=300, bbox_inches='tight')