# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 17

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# Define category levels based on the code structure
def get_category_level(category):
    code = category.split()[0]
    if code == '000000':
        return 'Overall'
    elif code.endswith('0000'):
        return 'Main Category'
    elif code.endswith('00'):
        return 'Subcategory'
    else:
        return 'Detailed Item'

# Add category level to the data
recent_data['CategoryLevel'] = recent_data['ExpenditureCategories'].apply(get_category_level)

# Clean category names for display
recent_data['CategoryName'] = recent_data['ExpenditureCategories'].str.extract(r'\d{6}\s+(.*)')

# Sort by category level and then by DerivedCPI value
level_order = ['Overall', 'Main Category', 'Subcategory', 'Detailed Item']
recent_data['LevelOrder'] = recent_data['CategoryLevel'].apply(lambda x: level_order.index(x))
recent_data = recent_data.sort_values(['LevelOrder', 'DerivedCPI_2'], ascending=[True, False])

# Select top categories from each level for better visualization
selected_data = pd.DataFrame()
for level in level_order:
    level_data = recent_data[recent_data['CategoryLevel'] == level]
    # Take all for Overall and Main Category, but limit others
    if level in ['Overall', 'Main Category']:
        selected_data = pd.concat([selected_data, level_data])
    else:
        # Take top 5 from each subcategory level
        selected_data = pd.concat([selected_data, level_data.head(5)])

# Create a custom color palette for the different levels
colors = {
    'Overall': '#1f77b4',       # Blue
    'Main Category': '#ff7f0e', # Orange
    'Subcategory': '#2ca02c',   # Green
    'Detailed Item': '#d62728'  # Red
}

# Create the plot
plt.figure(figsize=(16, 10))
sns.set_style("whitegrid")

# Create the bar plot with color based on category level
ax = sns.barplot(
    x='CategoryName', 
    y='DerivedCPI_2', 
    hue='CategoryLevel',
    data=selected_data, 
    palette=colors,
    hue_order=level_order
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

# Print information about the data used
print(f"\nVisualization saved with {len(selected_data)} product categories.")
print("\nCategories included in the plot:")
for i, (_, row) in enumerate(selected_data.iterrows()):
    print(f"{i+1}. {row['ExpenditureCategories']} - {row['CategoryName']} ({row['CategoryLevel']})")