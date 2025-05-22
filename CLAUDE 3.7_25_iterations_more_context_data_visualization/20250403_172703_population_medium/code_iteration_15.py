# Automatically saved code from agent execution
# Run ID: 20250403_172703_population_medium, Iteration: 15

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

# Remove 'Total' and 'Dutch background' from the list if they exist
backgrounds_to_remove = ['Total', 'Dutch background']
for bg in backgrounds_to_remove:
    if bg in top_backgrounds:
        top_backgrounds.remove(bg)

# Filter for these top backgrounds, 'Total', and 'Dutch background'
df_plot = df_filtered[df_filtered['MigrationBackground'].isin(top_backgrounds + ['Total', 'Dutch background'])]

# Create a pivot table for easier plotting
pivot_df = df_plot.pivot_table(
    index='Periods', 
    columns='MigrationBackground', 
    values='Population_1',
    aggfunc='sum'
)

# Create a figure with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 15), gridspec_kw={'height_ratios': [1, 1, 2]})

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

# Plot 2: Dutch background population
pivot_df['Dutch background'].plot(ax=ax2, marker='o', linewidth=2.5, color='navy')
ax2.set_title('Population with Dutch Background (2000-2010)', fontsize=16)
ax2.set_xlabel('')  # No x-label for the middle plot
ax2.set_ylabel('Population', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='both', labelsize=12)

# Add annotations for the Dutch background population
for year, value in pivot_df['Dutch background'].items():
    ax2.annotate(f'{int(value):,}', 
                xy=(year, value),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                fontsize=10)

# Plot 3: Population trends by other migration backgrounds
other_backgrounds_df = pivot_df.drop(['Total', 'Dutch background'], axis=1)
other_backgrounds_df.plot(ax=ax3, marker='o', linewidth=2.5)
ax3.set_title('Population by Other Migration Backgrounds (2000-2010)', fontsize=16)
ax3.set_xlabel('Year', fontsize=14)
ax3.set_ylabel('Population', fontsize=14)
ax3.grid(True, alpha=0.3)
ax3.tick_params(axis='both', labelsize=12)
ax3.legend(title='Migration Background', fontsize=11, title_fontsize=12)

# Calculate growth rates
growth_rates = {}
for bg in pivot_df.columns:
    start_val = pivot_df[bg].iloc[0]
    end_val = pivot_df[bg].iloc[-1]
    growth_rate = ((end_val - start_val) / start_val) * 100
    growth_rates[bg] = growth_rate

# Add a note about the data limitations
plt.figtext(0.5, 0.01, 
         "Note: The dataset does not contain breakdowns by marital status and sex as requested.",
         ha='center', fontsize=12, style='italic')

# Add growth rate information as text
growth_text = "Population Growth Rates (2000-2010):\n"
growth_text += f"Total: {growth_rates['Total']:.1f}%  |  Dutch background: {growth_rates['Dutch background']:.1f}%\n"

# Split other backgrounds into two lines for better readability
other_bgs = [bg for bg in sorted(growth_rates.keys()) if bg not in ['Total', 'Dutch background']]
half = len(other_bgs) // 2
first_half = other_bgs[:half]
second_half = other_bgs[half:]

for bg in first_half:
    growth_text += f"{bg}: {growth_rates[bg]:.1f}%  |  "
growth_text = growth_text.rstrip("  |  ") + "\n"

for bg in second_half:
    growth_text += f"{bg}: {growth_rates[bg]:.1f}%  |  "
growth_text = growth_text.rstrip("  |  ")

plt.figtext(0.5, 0.04, growth_text, ha='center', fontsize=11)

# Adjust layout and save
plt.tight_layout()
plt.subplots_adjust(hspace=0.3, bottom=0.1)
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172703_population_medium/visualization.png', dpi=300)
plt.close()