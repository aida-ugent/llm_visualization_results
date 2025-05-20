# Automatically saved code from agent execution
# Run ID: 20250403_165131_caribbean_births_easy, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the plot
plt.style.use('seaborn-v0_8-whitegrid')

# Load the data
data = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/caribbean_births.csv')

# Filter for Caribbean Netherlands only (in case there are other regions)
data = data[data['CaribbeanNetherlands'] == 'Caribbean Netherlands']

# Convert Periods to numeric to ensure proper ordering
data['Periods'] = pd.to_numeric(data['Periods'])

# Sort by year to ensure chronological order
data = data.sort_values('Periods')

# Create the figure and axis
plt.figure(figsize=(12, 6))

# Plot the line graph
plt.plot(data['Periods'], data['LiveBornChildren_1'], marker='o', linewidth=2, color='#1f77b4')

# Add labels and title
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Live Born Children', fontsize=12)
plt.title('Total Live Born Children in Caribbean Netherlands (2011-onwards)', fontsize=14, fontweight='bold')

# Format the x-axis to show all years
plt.xticks(data['Periods'], rotation=45)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add data points labels
for x, y in zip(data['Periods'], data['LiveBornChildren_1']):
    plt.text(x, y + 5, f'{int(y)}', ha='center', va='bottom', fontsize=9)

# Enhance the appearance
plt.tight_layout()

# Add a subtle annotation about data source
plt.figtext(0.5, 0.01, 'Data source: Caribbean Netherlands Statistics', 
            ha='center', fontsize=8, style='italic')

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165131_caribbean_births_easy/visualization.png', dpi=300, bbox_inches='tight')

# Close the plot to free memory
plt.close()