# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 16

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

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

# Let's look at all categories in the recent data
all_categories = recent_data['ExpenditureCategories'].unique()
print(f"Total unique categories in {most_recent_period}: {len(all_categories)}")

# Let's examine all categories to understand the structure better
print("\nExamining all categories:")
for cat in sorted(all_categories):
    print(f"  {cat}")

# Let's select a diverse set of categories for our visualization
# We'll exclude "All items" and select categories with different prefixes
selected_categories = []

# Exclude "All items" category
filtered_categories = [cat for cat in all_categories if 'All items' not in cat]

# Get the first 2 digits of each category code to identify different groups
category_groups = {}
for cat in filtered_categories:
    code = cat.split()[0]
    prefix = code[:2]
    if prefix not in category_groups:
        category_groups[prefix] = []
    category_groups[prefix].append(cat)

print(f"\nFound {len(category_groups)} different category groups:")
for prefix, cats in category_groups.items():
    print(f"  Group {prefix}: {len(cats)} categories")

# Select one category from each group (preferably a main category if available)
for prefix, cats in category_groups.items():
    # Try to find a main category (ending with 0000)
    main_cats = [cat for cat in cats if cat.split()[0].endswith('0000')]
    if main_cats:
        selected_categories.append(main_cats[0])
    # If no main category, try to find a second-level category (ending with 00)
    elif any(cat.split()[0].endswith('00') for cat in cats):
        second_level = [cat for cat in cats if cat.split()[0].endswith('00')]
        selected_categories.append(second_level[0])
    # Otherwise, just take the first category
    elif cats:
        selected_categories.append(cats[0])

# Get the data for selected categories
selected_data = recent_data[recent_data['ExpenditureCategories'].isin(selected_categories)]

# Clean category names for display
selected_data['CategoryName'] = selected_data['ExpenditureCategories'].str.extract(r'\d{6}\s+(.*)')

# Sort by DerivedCPI value
selected_data = selected_data.sort_values('DerivedCPI_2', ascending=False)

# Print the categories we'll be plotting
print(f"\nPlotting {len(selected_data)} categories:")
for i, (_, row) in enumerate(selected_data.iterrows()):
    print(f"{i+1}. {row['ExpenditureCategories']} - DerivedCPI: {row['DerivedCPI_2']}")

# Create the plot
plt.figure(figsize=(16, 10))
sns.set_style("whitegrid")

# Create the bar plot
ax = sns.barplot(
    x='CategoryName', 
    y='DerivedCPI_2', 
    data=selected_data, 
    palette='viridis'
)

# Add labels and title
plt.title(f'Derived Consumer Price Index by Product Category\n(Period: {most_recent_period})', fontsize=16)
plt.xlabel('Product Category', fontsize=14)
plt.ylabel('Derived CPI', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Add data labels on top of bars
for i, v in enumerate(selected_data['DerivedCPI_2']):
    ax.text(i, v + 1, f'{v:.1f}', ha='center', fontsize=9)

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165909_consumer_prices_medium/visualization.png', dpi=300, bbox_inches='tight')

print(f"\nVisualization saved with {len(selected_data)} product categories.")