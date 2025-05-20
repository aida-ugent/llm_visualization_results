# Automatically saved code from agent execution
# Run ID: 20250403_172534_population_medium, Iteration: 8

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

# Get data for specific countries
# Exclude high-level categories and continents
exclude_categories = main_categories + ['Total', 'Africa', 'America', 'Asia', 
                                       'Europe (excluding Dutch background)', 'Oceania', 
                                       'European Union (excl. Dutch background)',
                                       'GIPS countries (European Union)',
                                       'Middle and Eastern European EU countries',
                                       'Unknown migration background']

country_population = df_2010[(df_2010['Sex'] == 'Total males and females') & 
                            (df_2010['Age'] == 'Total') & 
                            (df_2010['MaritalStatus'] == 'Total') &
                            (df_2010['Generation'] == 'Total') &
                            (~df_2010['MigrationBackground'].isin(exclude_categories))]

# Get top 10 countries by population
top_countries = country_population.sort_values('Population_1', ascending=False).head(10)

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

# Create a horizontal bar chart for top 10 countries
bars = ax2.barh(
    top_countries['MigrationBackground'][::-1],  # Reverse order to have largest at top
    top_countries['Population_1'][::-1],
    color=sns.color_palette('Set2', n_colors=len(top_countries)),
    edgecolor='white',
    linewidth=1
)

# Add data labels to the bars
for bar in bars:
    width = bar.get_width()
    ax2.text(
        width + 5000,  # Offset from the end of the bar
        bar.get_y() + bar.get_height()/2,
        f'{width:,.0f}',
        va='center',
        fontsize=10
    )

# Set title and labels for the second subplot
ax2.set_title('Top 10 Countries of Origin (2010)', fontsize=16)
ax2.set_xlabel('Population', fontsize=12)
ax2.grid(axis='x', linestyle='--', alpha=0.7)

# Remove top and right spines
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

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

# Ensure a tight layout
plt.tight_layout(rect=[0, 0.1, 1, 0.95])

# Save the figure
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172534_population_medium/visualization.png', 
            dpi=300, bbox_inches='tight')