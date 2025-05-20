# Automatically saved code from agent execution
# Run ID: 20250403_165421_caribbean_births_medium, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data_path = '/Users/alexanderrogiers/ugent/llm_visualization/data/caribbean_births.csv'
df = pd.read_csv(data_path)

# Filter for Caribbean Netherlands data
df = df[df['CaribbeanNetherlands'] == 'Caribbean Netherlands']

# Extract the relevant columns for women over 40
years = df['Periods'].astype(int)
births_40_to_44 = df['k_40To44Years_14']
births_45_plus = df['k_45YearsOrOlder_15']

# Create a stacked bar chart
fig, ax = plt.subplots(figsize=(12, 7))

# Plot the stacked bars
bar_width = 0.7
bars1 = ax.bar(years, births_40_to_44, bar_width, label='40-44 Years')
bars2 = ax.bar(years, births_45_plus, bar_width, bottom=births_40_to_44, label='45+ Years')

# Calculate total births from women over 40 for annotations
total_births = births_40_to_44 + births_45_plus

# Add data labels on top of each bar
for i, (y, total) in enumerate(zip(years, total_births)):
    ax.text(y, total + 0.5, f'{int(total)}', ha='center', va='bottom', fontweight='bold')

# Customize the plot
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Live Births', fontsize=12)
ax.set_title('Live Births from Women Older Than 40 in Caribbean Netherlands (2011-2023)', fontsize=14, fontweight='bold')
ax.legend(title='Age Group')

# Set the y-axis to start from 0
ax.set_ylim(bottom=0)

# Add grid lines for better readability
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Ensure x-axis shows all years
ax.set_xticks(years)
ax.set_xticklabels(years, rotation=45)

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165421_caribbean_births_medium/visualization.png', dpi=300)