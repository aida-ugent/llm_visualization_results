# Automatically saved code from agent execution
# Run ID: 20250403_165156_caribbean_births_medium, Iteration: 6

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/caribbean_births.csv')

# Find the most recent year in the data
most_recent_year = df['Periods'].max()
print(f"Most recent year in the dataset: {most_recent_year}")

# Filter data for the most recent year
recent_data = df[df['Periods'] == most_recent_year]

# Select only the regions (not the aggregate "Caribbean Netherlands")
regions_data = recent_data[recent_data['CaribbeanNetherlands'] != 'Caribbean Netherlands']

# Create a new DataFrame for plotting
plot_data = pd.DataFrame({
    'Region': regions_data['CaribbeanNetherlands'],
    'Boys': regions_data['LiveBornBoys_3'],
    'Girls': regions_data['LiveBornGirls_4']
})

# Reshape the data for seaborn
plot_data_melted = pd.melt(
    plot_data, 
    id_vars=['Region'], 
    value_vars=['Boys', 'Girls'],
    var_name='Gender', 
    value_name='Number of Newborns'
)

# Set up the figure with a larger size
plt.figure(figsize=(12, 8))

# Create a grouped bar chart
sns.set_style("whitegrid")
ax = sns.barplot(
    x='Region', 
    y='Number of Newborns', 
    hue='Gender', 
    data=plot_data_melted,
    palette=['#1f77b4', '#ff7f0e']  # Blue for boys, orange for girls
)

# Add value labels on top of each bar
for p in ax.patches:
    ax.annotate(
        f'{p.get_height():.0f}',
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', 
        va='bottom',
        fontsize=11,
        fontweight='bold'
    )

# Add a title and labels
plt.title(f'Distribution of Newborn Boys and Girls in Caribbean Netherlands ({most_recent_year})', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Region', fontsize=14, labelpad=10)
plt.ylabel('Number of Newborns', fontsize=14, labelpad=10)

# Add the total number of newborns for each region
for i, region in enumerate(plot_data['Region']):
    boys = plot_data.loc[i, 'Boys']
    girls = plot_data.loc[i, 'Girls']
    total = boys + girls
    plt.text(i, 5, f'Total: {total:.0f}', ha='center', fontsize=12, fontweight='bold')

# Enhance the legend
plt.legend(title='Gender', fontsize=12, title_fontsize=13)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165156_caribbean_births_medium/visualization.png', dpi=300, bbox_inches='tight')

# Show the plot (this won't be visible in the execution environment but is good practice)
plt.close()

# Print some additional information about the data
print("\nSummary of newborn distribution by region for", most_recent_year)
for i, row in plot_data.iterrows():
    region = row['Region']
    boys = row['Boys']
    girls = row['Girls']
    total = boys + girls
    boy_percentage = (boys / total) * 100
    girl_percentage = (girls / total) * 100
    print(f"{region}: {boys:.0f} boys ({boy_percentage:.1f}%), {girls:.0f} girls ({girl_percentage:.1f}%), Total: {total:.0f}")