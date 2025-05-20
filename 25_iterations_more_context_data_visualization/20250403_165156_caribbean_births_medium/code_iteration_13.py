# Automatically saved code from agent execution
# Run ID: 20250403_165156_caribbean_births_medium, Iteration: 13

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

# Calculate totals
plot_data['Total'] = plot_data['Boys'] + plot_data['Girls']

# Calculate percentages
for idx in plot_data.index:
    total = plot_data.loc[idx, 'Total']
    plot_data.loc[idx, 'Boys_Percentage'] = round((plot_data.loc[idx, 'Boys'] / total) * 100, 1)
    plot_data.loc[idx, 'Girls_Percentage'] = round((plot_data.loc[idx, 'Girls'] / total) * 100, 1)

# Set up the figure with a larger size
plt.figure(figsize=(14, 10))

# Create a grouped bar chart manually for more control
bar_width = 0.35
x = np.arange(len(plot_data))

# Create bars
boys_bars = plt.bar(x - bar_width/2, plot_data['Boys'], bar_width, label='Boys', color='#3274A1')
girls_bars = plt.bar(x + bar_width/2, plot_data['Girls'], bar_width, label='Girls', color='#E1812C')

# Add value labels on top of each bar with percentages
for i, bar in enumerate(boys_bars):
    height = bar.get_height()
    percentage = plot_data.iloc[i]['Boys_Percentage']
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f'{height:.0f}\n({percentage}%)',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

for i, bar in enumerate(girls_bars):
    height = bar.get_height()
    percentage = plot_data.iloc[i]['Girls_Percentage']
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f'{height:.0f}\n({percentage}%)',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add a title and labels
plt.title(f'Distribution of Newborn Boys and Girls in Caribbean Netherlands ({most_recent_year})', 
          fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Region', fontsize=16, labelpad=15)
plt.ylabel('Number of Newborns', fontsize=16, labelpad=15)

# Set x-axis ticks
plt.xticks(x, plot_data['Region'], fontsize=14)

# Add the total number of newborns for each region
for i, row in plot_data.iterrows():
    plt.text(i, -10, f'Total: {row["Total"]:.0f}', ha='center', fontsize=14, fontweight='bold')

# Add grid lines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Enhance the legend
plt.legend(title='Gender', fontsize=14, title_fontsize=16)

# Add a text box with summary information
total_births = plot_data['Total'].sum()
total_boys = plot_data['Boys'].sum()
total_girls = plot_data['Girls'].sum()
boy_percentage = round((total_boys / total_births) * 100, 1)
girl_percentage = round((total_girls / total_births) * 100, 1)

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