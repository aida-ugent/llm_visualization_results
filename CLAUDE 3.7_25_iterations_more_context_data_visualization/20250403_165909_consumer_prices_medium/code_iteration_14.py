# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 14

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

# Let's select a diverse set of categories for our visualization
# We'll exclude "All items" and focus on specific product categories
selected_categories = []

# Function to check if a category is a main category (ends with 0000)
def is_main_category(category):
    code = category.split()[0]
    return code.endswith('0000') and not category.startswith('000000')

# Function to check if a category is a second-level category (ends with 00 but not 0000)
def is_second_level(category):
    code = category.split()[0]
    return code.endswith('00') and not code.endswith('0000')

# Get main categories (excluding "All items")
main_cats = [cat for cat in all_categories if is_main_category(cat) and 'All items' not in cat]
print(f"Main categories: {len(main_cats)}")

# Get second-level categories
second_level_cats = [cat for cat in all_categories if is_second_level(cat)]
print(f"Second-level categories: {len(second_level_cats)}")

# Select categories for visualization
# First, add all main categories
selected_categories.extend(main_cats)

# Then add some second-level categories (limit to keep visualization readable)
selected_categories.extend(second_level_cats[:9])  # Limit to 9 second-level categories

# Get the data for selected categories
selected_data = recent_data[recent_data['ExpenditureCategories'].isin(selected_categories)]

# Clean category names for display
selected_data['CategoryName'] = selected_data['ExpenditureCategories'].str.extract(r'\d{6}\s+(.*)')

# Determine category level for coloring
selected_data['CategoryLevel'] = np.where(
    selected_data['ExpenditureCategories'].apply(is_main_category), 
    'Main Category', 
    'Subcategory'
)

# Sort by DerivedCPI value
selected_data = selected_data.sort_values('DerivedCPI_2', ascending=False)

# Print the categories we'll be plotting
print(f"\nPlotting {len(selected_data)} categories:")
for i, (_, row) in enumerate(selected_data.iterrows()):
    print(f"{i+1}. {row['ExpenditureCategories']} ({row['CategoryLevel']}) - DerivedCPI: {row['DerivedCPI_2']}")

# Create the plot
plt.figure(figsize=(16, 10))
sns.set_style("whitegrid")

# Create the bar plot with color based on category level
ax = sns.barplot(
    x='CategoryName', 
    y='DerivedCPI_2', 
    hue='CategoryLevel',
    data=selected_data, 
    palette={'Main Category': '#1f77b4', 'Subcategory': '#2ca02c'}
)

# Add labels and title
plt.title(f'Derived Consumer Price Index by Product Category\n(Period: {most_recent_period})', fontsize=16)
plt.xlabel('Product Category', fontsize=14)
plt.ylabel('Derived CPI', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Category Type')
plt.tight_layout()

# Add data labels on top of bars
for i, v in enumerate(selected_data['DerivedCPI_2']):
    ax.text(i, v + 1, f'{v:.1f}', ha='center', fontsize=9)

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165909_consumer_prices_medium/visualization.png', dpi=300, bbox_inches='tight')

print(f"\nVisualization saved with {len(selected_data)} product categories.")