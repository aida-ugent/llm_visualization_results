# Automatically saved code from agent execution
# Run ID: 20250403_172534_population_medium, Iteration: 6

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for the year 2010
df_2010 = df[df['Periods'] == 2010]

# Get data for main migration background categories
main_categories = ['Dutch background', 'Western migration background', 'Non-western migration background']

# Filter for total population by main migration background categories
main_population = df_2010[(df_2010['Sex'] == 'Total males and females') & 
                         (df_2010['Age'] == 'Total') & 
                         (df_2010['MaritalStatus'] == 'Total') &
                         (df_2010['Generation'] == 'Total') &
                         (df_2010['MigrationBackground'].isin(main_categories))]

# Get data for specific regions (continents and major regions)
region_categories = ['Africa', 'America', 'Asia', 'Europe (excluding Dutch background)', 
                    'Oceania', 'European Union (excl. Dutch background)']

region_population = df_2010[(df_2010['Sex'] == 'Total males and females') & 
                           (df_2010['Age'] == 'Total') & 
                           (df_2010['MaritalStatus'] == 'Total') &
                           (df_2010['Generation'] == 'Total') &
                           (df_2010['MigrationBackground'].isin(region_categories))]

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

# Colors for the main pie chart
main_colors = sns.color_palette('pastel', n_colors=len(main_population))

# Create the main pie chart
wedges, texts, autotexts = ax1.pie(
    main_population['Population_1'], 
    labels=main_population['MigrationBackground'],
    autopct='%1.1f%%',
    startangle=90,
    explode=[0.05, 0.05, 0.05],  # Slightly explode all slices
    colors=main_colors,
    textprops={'fontsize': 12},
    wedgeprops={'edgecolor': 'w', 'linewidth': 1}
)

# Enhance the appearance of the text
for autotext in autotexts:
    autotext.set_fontweight('bold')

# Set title for the first subplot
ax1.set_title('Population by Migration Background (2010)', fontsize=16)

# Colors for the region pie chart
region_colors = sns.color_palette('Set2', n_colors=len(region_population))

# Sort region population by size for better visualization
region_population = region_population.sort_values('Population_1', ascending=False)

# Create the region pie chart
wedges, texts, autotexts = ax2.pie(
    region_population['Population_1'], 
    labels=region_population['MigrationBackground'],
    autopct='%1.1f%%',
    startangle=90,
    explode=[0.05] * len(region_population),  # Slightly explode all slices
    colors=region_colors,
    textprops={'fontsize': 12},
    wedgeprops={'edgecolor': 'w', 'linewidth': 1}
)

# Enhance the appearance of the text
for autotext in autotexts:
    autotext.set_fontweight('bold')

# Set title for the second subplot
ax2.set_title('Population by Region of Origin (2010)', fontsize=16)

# Add a main title for the entire figure
fig.suptitle('Population Distribution by Migration Background in the Netherlands (2010)', 
             fontsize=20, y=0.98)

# Add a note with the total population
total_population = df_2010[df_2010['MigrationBackground'] == 'Total']['Population_1'].values[0]
fig.text(0.5, 0.01, 
         f'Total Population in 2010: {total_population:,.0f}',
         ha='center', fontsize=14)

# Add a note with the actual numbers for main categories
y_pos = 0.08
for _, row in main_population.iterrows():
    fig.text(0.25, y_pos, 
             f"{row['MigrationBackground']}: {row['Population_1']:,.0f}",
             ha='center', fontsize=11)
    y_pos += 0.03

# Add a note with the actual numbers for region categories
y_pos = 0.08
for _, row in region_population.iterrows():
    fig.text(0.75, y_pos, 
             f"{row['MigrationBackground']}: {row['Population_1']:,.0f}",
             ha='center', fontsize=11)
    y_pos += 0.03

# Ensure a tight layout
plt.tight_layout(rect=[0, 0.1, 1, 0.95])

# Save the figure
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172534_population_medium/visualization.png', 
            dpi=300, bbox_inches='tight')