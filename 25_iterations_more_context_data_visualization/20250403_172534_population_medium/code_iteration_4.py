# Automatically saved code from agent execution
# Run ID: 20250403_172534_population_medium, Iteration: 4

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv')

# Filter for the year 2010
df_2010 = df[df['Periods'] == 2010]

# Get data for main migration background categories
# We'll focus on the high-level categories for clarity
main_categories = ['Dutch background', 'Western migration background', 'Non-western migration background']

# Filter for total population by main migration background categories
population_by_background = df_2010[(df_2010['Sex'] == 'Total males and females') & 
                                  (df_2010['Age'] == 'Total') & 
                                  (df_2010['MaritalStatus'] == 'Total') &
                                  (df_2010['Generation'] == 'Total') &
                                  (df_2010['MigrationBackground'].isin(main_categories))]

# Create a figure with appropriate size
plt.figure(figsize=(12, 8))

# Create a pie chart
plt.pie(population_by_background['Population_1'], 
        labels=population_by_background['MigrationBackground'],
        autopct='%1.1f%%',
        startangle=90,
        explode=[0.05, 0.05, 0.05],  # Slightly explode all slices
        colors=sns.color_palette('pastel'),
        textprops={'fontsize': 12})

# Add a title and subtitle
plt.title('Population Distribution by Migration Background in the Netherlands (2010)', 
          fontsize=16, pad=20)
plt.figtext(0.5, 0.01, 
            f'Total Population in 2010: {df_2010[df_2010["MigrationBackground"] == "Total"]["Population_1"].values[0]:,.0f}',
            ha='center', fontsize=12)

# Ensure a tight layout
plt.tight_layout()

# Save the figure
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172534_population_medium/visualization.png', 
            dpi=300, bbox_inches='tight')

# Show the actual values for reference
print("Population by Migration Background in 2010:")
for _, row in population_by_background.iterrows():
    print(f"{row['MigrationBackground']}: {row['Population_1']:,.0f}")

# Calculate percentages
total = population_by_background['Population_1'].sum()
for _, row in population_by_background.iterrows():
    percentage = (row['Population_1'] / total) * 100
    print(f"{row['MigrationBackground']}: {percentage:.1f}%")