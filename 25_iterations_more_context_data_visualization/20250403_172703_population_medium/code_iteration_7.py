# Automatically saved code from agent execution
# Run ID: 20250403_172703_population_medium, Iteration: 7

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for the years 2000 to 2010
df_filtered = df[(df['Periods'] >= 2000) & (df['Periods'] <= 2010)]

# Since we don't have the specific breakdowns by marital status and sex,
# let's look at the population trends by migration background
# First, let's identify the top migration backgrounds by population
migration_totals = df_filtered.groupby('MigrationBackground')['Population_1'].sum().sort_values(ascending=False)
top_backgrounds = migration_totals.head(6).index.tolist()

# Remove 'Total' from the list if it exists
if 'Total' in top_backgrounds:
    top_backgrounds.remove('Total')

# Add 'Total' as a separate category
top_backgrounds = ['Total'] + top_backgrounds

# Filter for these top backgrounds
df_plot = df_filtered[df_filtered['MigrationBackground'].isin(top_backgrounds)]

# Create a pivot table for easier plotting
pivot_df = df_plot.pivot_table(
    index='Periods', 
    columns='MigrationBackground', 
    values='Population_1',
    aggfunc='sum'
)

# Create the plot
plt.figure(figsize=(14, 8))
ax = pivot_df.plot(marker='o', linewidth=2.5, figsize=(14, 8))

# Customize the plot
plt.title('Population Trends in the Netherlands by Migration Background (2000-2010)', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Population', fontsize=14)
plt.grid(True, alpha=0.3)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='Migration Background', fontsize=12, title_fontsize=13)

# Add annotations for the total population
for year, value in pivot_df['Total'].items():
    ax.annotate(f'{int(value):,}', 
                xy=(year, value),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                fontsize=9)

# Adjust layout and save
plt.tight_layout()
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172703_population_medium/visualization.png', dpi=300)
plt.close()