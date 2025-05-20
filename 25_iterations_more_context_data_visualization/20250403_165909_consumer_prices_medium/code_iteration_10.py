# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 10

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Let's find more main categories by looking at the patterns in the data
print("Analyzing category patterns...")

# Check for patterns in the expenditure categories
patterns = []
for cat in df['ExpenditureCategories'].unique():
    code = cat.split()[0]
    if code.endswith('0000'):
        patterns.append(code)

print(f"Found {len(set(patterns))} potential main categories")

# Let's get all categories that end with 0000 (main categories)
main_cats = df[df['ExpenditureCategories'].str.contains(r'\d{2}0000')]
main_cat_codes = main_cats['ExpenditureCategories'].unique()
print(f"Number of main categories: {len(main_cat_codes)}")

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

# Filter for main categories in the most recent period
main_recent = recent_data[recent_data['ExpenditureCategories'].str.contains(r'\d{2}0000')]

# Clean category names for display and exclude "All items"
main_recent = main_recent[~main_recent['ExpenditureCategories'].str.contains('All items')]
main_recent['CategoryName'] = main_recent['ExpenditureCategories'].str.extract(r'\d{6}\s+(.*)')

# Sort by DerivedCPI value
main_recent = main_recent.sort_values('DerivedCPI_2', ascending=False)

# Print the categories we'll be plotting
print(f"\nPlotting {len(main_recent)} main categories:")
for i, (_, row) in enumerate(main_recent.iterrows()):
    print(f"{i+1}. {row['ExpenditureCategories']} - DerivedCPI: {row['DerivedCPI_2']}")

# Create the plot
plt.figure(figsize=(14, 10))
sns.set_style("whitegrid")

# Create the bar plot
ax = sns.barplot(
    x='CategoryName', 
    y='DerivedCPI_2', 
    data=main_recent, 
    palette='viridis'
)

# Add labels and title
plt.title(f'Derived Consumer Price Index by Main Product Category\n(Period: {most_recent_period})', fontsize=16)
plt.xlabel('Product Category', fontsize=14)
plt.ylabel('Derived CPI', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Add data labels on top of bars
for i, v in enumerate(main_recent['DerivedCPI_2']):
    ax.text(i, v + 1, f'{v:.1f}', ha='center', fontsize=9)

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165909_consumer_prices_medium/visualization.png', dpi=300, bbox_inches='tight')

print(f"\nVisualization saved with {len(main_recent)} main product categories.")