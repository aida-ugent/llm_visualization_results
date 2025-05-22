# Automatically saved code from agent execution
# Run ID: 20250403_165456_caribbean_births_hard, Iteration: 6

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the plot
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/caribbean_births.csv')

# Filter data for Bonaire in 2015
bonaire_2015 = df[(df['CaribbeanNetherlands'] == 'Bonaire') & (df['Periods'] == 2015)]

# Extract the marital status data
marital_status = {
    'Married': bonaire_2015['MotherMarried_22'].values[0],
    'Never Married': bonaire_2015['MotherNeverMarried_23'].values[0]
}

# Create a DataFrame for plotting
plot_df = pd.DataFrame({
    'Marital Status': list(marital_status.keys()),
    'Number of Live-Born Children': list(marital_status.values())
})

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Create the bar plot
bars = sns.barplot(x='Marital Status', y='Number of Live-Born Children', data=plot_df, ax=ax)

# Add data labels on top of each bar
for i, bar in enumerate(bars.patches):
    bars.text(
        bar.get_x() + bar.get_width()/2.,
        bar.get_height() + 5,
        f'{int(bar.get_height())}',
        ha='center',
        fontsize=12,
        fontweight='bold'
    )

# Set the title and labels
plt.title('Number of Live-Born Children by Marital Status in Bonaire (2015)', fontsize=16, pad=20)
plt.xlabel('Marital Status of Mother', fontsize=14)
plt.ylabel('Number of Live-Born Children', fontsize=14)

# Add a text annotation with the total
total = marital_status['Married'] + marital_status['Never Married']
plt.annotate(f'Total: {int(total)} children', xy=(0.5, 0.9), xycoords='axes fraction', 
             ha='center', fontsize=12, bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="gray", alpha=0.8))

# Customize the y-axis to start from 0
plt.ylim(0, max(marital_status.values()) * 1.2)

# Add grid lines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add a percentage annotation to each bar
for i, (status, count) in enumerate(marital_status.items()):
    percentage = (count / total) * 100
    plt.annotate(f'{percentage:.1f}%', 
                 xy=(i, count/2), 
                 ha='center',
                 va='center',
                 fontsize=12,
                 fontweight='bold',
                 color='white')

# Improve the overall appearance
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165456_caribbean_births_hard/visualization.png', dpi=300, bbox_inches='tight')

# Show the plot (this won't be visible in the execution environment but is good practice)
plt.close()