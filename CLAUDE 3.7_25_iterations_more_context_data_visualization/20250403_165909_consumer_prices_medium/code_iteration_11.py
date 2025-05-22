# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 11

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Let's find more categories by looking at different patterns
print("Analyzing category patterns...")

# Check for different category levels
level1_pattern = r'^\d{2}0000\s'  # Main categories like "010000 Food and non-alcoholic beverages"
level2_pattern = r'^\d{4}00\s'    # Second-level categories like "011000 Food"
level3_pattern = r'^\d{6}\s'      # Detailed categories that don't match the above patterns

# Count categories at each level
level1_cats = df[df['ExpenditureCategories'].str.match(level1_pattern)]
level2_cats = df[df['ExpenditureCategories'].str.match(level2_pattern) & 
                ~df['ExpenditureCategories'].str.match(level1_pattern)]
level3_cats = df[df['ExpenditureCategories'].str.match(level3_pattern) & 
                ~df['ExpenditureCategories'].str.match(level1_pattern) & 
                ~df['ExpenditureCategories'].str.match(level2_pattern)]

print(f"Level 1 (Main) categories: {len(level1_cats['ExpenditureCategories'].unique())}")
print(f"Level 2 categories: {len(level2_cats['ExpenditureCategories'].unique())}")
print(f"Level 3 categories: {len(level3_cats['ExpenditureCategories'].unique())}")

# Get the most recent period
periods = sorted(df['Periods'].unique())
most_recent_period = periods[-1]
print(f"Most recent period: {most_recent_period}")

# Get data for the most recent period
recent_data = df[df['Periods'] == most_recent_period]

# If there's no data for the most recent period, try the second most recent
if recent_data.empty:
    most_recent_period = periods[-2]
    recent_data = df[df['Periods'] == most_recent_period]
    print(f"Using second most recent period: {most_recent_period}")

# Filter for level 2 categories in the most recent period (more detailed than main categories)
level2_recent = recent_data[recent_data['ExpenditureCategories'].str.match(level2_pattern) & 
                           ~recent_data['ExpenditureCategories'].str.match(level1_pattern)]

# Clean category names for display
level2_recent['CategoryName'] = level2_recent['ExpenditureCategories'].str.extract(r'\d{6}\s+(.*)')

# Sort by DerivedCPI value
level2_recent = level2_recent.sort_values('DerivedCPI_2', ascending=False)

# Print the categories we'll be plotting
print(f"\nPlotting {len(level2_recent)} level 2 categories:")
for i, (_, row) in enumerate(level2_recent.iterrows()):
    print(f"{i+1}. {row['ExpenditureCategories']} - DerivedCPI: {row['DerivedCPI_2']}")

# Create the plot
plt.figure(figsize=(16, 10))
sns.set_style("whitegrid")

# Create the bar plot
ax = sns.barplot(
    x='CategoryName', 
    y='DerivedCPI_2', 
    data=level2_recent, 
    palette='viridis'
)

# Add labels and title
plt.title(f'Derived Consumer Price Index by Product Category\n(Period: {most_recent_period})', fontsize=16)
plt.xlabel('Product Category', fontsize=14)
plt.ylabel('Derived CPI', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Add data labels on top of bars
for i, v in enumerate(level2_recent['DerivedCPI_2']):
    ax.text(i, v + 1, f'{v:.1f}', ha='center', fontsize=9)

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165909_consumer_prices_medium/visualization.png', dpi=300, bbox_inches='tight')

print(f"\nVisualization saved with {len(level2_recent)} product categories.")