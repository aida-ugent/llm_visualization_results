# Automatically saved code from agent execution
# Run ID: 20250403_165156_caribbean_births_medium, Iteration: 11

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# Calculate totals and percentages
plot_data['Total'] = plot_data['Boys'] + plot_data['Girls']
plot_data['Boys_Percentage'] = (plot_data['Boys'] / plot_data['Total'] * 100).round(1)
plot_data['Girls_Percentage'] = (plot_data['Girls'] / plot_data['Total'] * 100).round(1)

# Reset index to ensure proper iteration
plot_data = plot_data.reset_index(drop=True)

# Reshape the data for seaborn
plot_data_melted = pd.melt(
    plot_data, 
    id_vars=['Region', 'Total', 'Boys_Percentage', 'Girls_Percentage'], 
    value_vars=['Boys', 'Girls'],
    var_name='Gender', 
    value_name='Number of Newborns'
)

# Set up the figure with a larger size
plt.figure(figsize=(14, 10))

# Create a grouped bar chart
sns.set_style("whitegrid")
ax = sns.barplot(
    x='Region', 
    y='Number of Newborns', 
    hue='Gender', 
    data=plot_data_melted,
    palette=['#3274A1', '#E1812C']  # Blue for boys, orange for girls
)

# Add value labels on top of each bar with percentages
for i, p in enumerate(ax.patches):
    # Get the index in the original dataframe
    idx = i // 2  # Integer division to get the region index
    gender = 'Boys' if i % 2 == 0 else 'Girls'
    percentage = plot_data.loc[idx, f'{gender}_Percentage']
    
    # Add count and percentage
    ax.annotate(
        f'{p.get_height():.0f}\n({percentage}%)',
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', 
        va='bottom',
        fontsize=11,
        fontweight='bold'
    )

# Add a title and labels
plt.title(f'Distribution of Newborn Boys and Girls in Caribbean Netherlands ({most_recent_year})', 
          fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Region', fontsize=16, labelpad=15)
plt.ylabel('Number of Newborns', fontsize=16, labelpad=15)

# Add the total number of newborns for each region
for i, row in plot_data.iterrows():
    plt.text(i, -15, f'Total: {row["Total"]:.0f}', ha='center', fontsize=14, fontweight='bold')

# Enhance the legend
plt.legend(title='Gender', fontsize=14, title_fontsize=16)

# Add a text box with summary information
total_births = plot_data['Total'].sum()
total_boys = plot_data['Boys'].sum()
total_girls = plot_data['Girls'].sum()
boy_percentage = (total_boys / total_births * 100).round(1)
girl_percentage = (total_girls / total_births * 100).round(1)

summary_text = (
    f"Total births in Caribbean Netherlands: {total_births:.0f}\n"
    f"Boys: {total_boys:.0f} ({boy_percentage}%)\n"
    f"Girls: {total_girls:.0f} ({girl_percentage}%)"
)

# Add a text box with the summary
plt.figtext(0.5, 0.01, summary_text, ha='center', fontsize=14, 
            bbox=dict(facecolor='#f0f0f0', alpha=0.5, boxstyle='round,pad=0.5'))

# Adjust layout and add more bottom margin for the total labels
plt.subplots_adjust(bottom=0.2)

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165156_caribbean_births_medium/visualization.png', dpi=300, bbox_inches='tight')

# Show the plot (this won't be visible in the execution environment but is good practice)
plt.close()

# Print some additional information about the data
print("\nSummary of newborn distribution by region for", most_recent_year)
for _, row in plot_data.iterrows():
    region = row['Region']
    boys = row['Boys']
    girls = row['Girls']
    total = row['Total']
    boy_percentage = row['Boys_Percentage']
    girl_percentage = row['Girls_Percentage']
    print(f"{region}: {boys:.0f} boys ({boy_percentage}%), {girls:.0f} girls ({girl_percentage}%), Total: {total:.0f}")

print(f"\nOverall: {total_boys:.0f} boys ({boy_percentage}%), {total_girls:.0f} girls ({girl_percentage}%), Total: {total_births:.0f}")