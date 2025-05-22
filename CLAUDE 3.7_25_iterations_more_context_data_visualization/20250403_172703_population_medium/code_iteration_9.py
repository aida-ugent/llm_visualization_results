# Automatically saved code from agent execution
# Run ID: 20250403_172703_population_medium, Iteration: 9

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for the years 2000 to 2010
df_filtered = df[(df['Periods'] >= 2000) & (df['Periods'] <= 2010)]

# Since we don't have the specific breakdowns by marital status and sex,
# let's look at the population trends by migration background
# First, let's identify the top migration backgrounds by population
migration_totals = df_filtered.groupby('MigrationBackground')['Population_1'].sum().sort_values(ascending=False)
top_backgrounds = migration_totals.head(10).index.tolist()

# Remove 'Total' from the list if it exists
if 'Total' in top_backgrounds:
    top_backgrounds.remove('Total')

# Filter for these top backgrounds and 'Total'
df_plot = df_filtered[df_filtered['MigrationBackground'].isin(top_backgrounds + ['Total'])]

# Create a pivot table for easier plotting
pivot_df = df_plot.pivot_table(
    index='Periods', 
    columns='MigrationBackground', 
    values='Population_1',
    aggfunc='sum'
)

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [1, 2]})

# Plot 1: Total population trend
pivot_df['Total'].plot(ax=ax1, marker='o', linewidth=2.5, color='darkred')
ax1.set_title('Total Population in the Netherlands (2000-2010)', fontsize=16)
ax1.set_xlabel('')  # No x-label for the top plot
ax1.set_ylabel('Population', fontsize=14)
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='both', labelsize=12)

# Add annotations for the total population
for year, value in pivot_df['Total'].items():
    ax1.annotate(f'{int(value):,}', 
                xy=(year, value),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                fontsize=10)

# Plot 2: Population trends by migration background (excluding Total)
pivot_df.drop('Total', axis=1).plot(ax=ax2, marker='o', linewidth=2.5)
ax2.set_title('Population by Migration Background (2000-2010)', fontsize=16)
ax2.set_xlabel('Year', fontsize=14)
ax2.set_ylabel('Population', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='both', labelsize=12)
ax2.legend(title='Migration Background', fontsize=12, title_fontsize=13)

# Add a note about the data limitations
fig.text(0.5, 0.01, 
         "Note: The dataset does not contain breakdowns by marital status and sex as requested.",
         ha='center', fontsize=12, style='italic')

# Adjust layout and save
plt.tight_layout()
plt.subplots_adjust(hspace=0.3, bottom=0.05)
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172703_population_medium/visualization.png', dpi=300)
plt.close()