# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 5

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Extract the main categories (those with 6-digit codes where the last 4 digits are zeros)
main_categories = df[df['ExpenditureCategories'].str.match(r'\d{2}0000.*')]

# Get the most recent period
most_recent_period = df['Periods'].max()

# Filter for the most recent period
recent_data = main_categories[main_categories['Periods'] == most_recent_period]

# If there's no data for the most recent period, try the second most recent
if recent_data.empty:
    periods = sorted(df['Periods'].unique())
    most_recent_period = periods[-1]
    recent_data = main_categories[main_categories['Periods'] == most_recent_period]

# If still empty, we need to take a different approach
if recent_data.empty:
    # Get the latest available data for each main category
    latest_data = []
    for category in main_categories['ExpenditureCategories'].unique():
        category_data = main_categories[main_categories['ExpenditureCategories'] == category]
        if not category_data.empty:
            latest_period = category_data['Periods'].max()
            latest_data.append(category_data[category_data['Periods'] == latest_period].iloc[0])
    
    if latest_data:
        recent_data = pd.DataFrame(latest_data)

# Clean category names for display
recent_data['CategoryName'] = recent_data['ExpenditureCategories'].str.extract(r'\d{6}\s+(.*)')

# Sort by DerivedCPI value
recent_data = recent_data.sort_values('DerivedCPI_2', ascending=False)

# Create the plot
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# Create the bar plot
ax = sns.barplot(x='CategoryName', y='DerivedCPI_2', data=recent_data, palette='viridis')

# Add labels and title
plt.title(f'Derived Consumer Price Index by Main Product Category\n(Period: {most_recent_period})', fontsize=16)
plt.xlabel('Product Category', fontsize=14)
plt.ylabel('Derived CPI', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Add data labels on top of bars
for i, v in enumerate(recent_data['DerivedCPI_2']):
    ax.text(i, v + 1, f'{v:.1f}', ha='center', fontsize=10)

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165909_consumer_prices_medium/visualization.png', dpi=300, bbox_inches='tight')

# Print information about the data used
print(f"Created bar graph using data from period: {most_recent_period}")
print(f"Number of main categories plotted: {len(recent_data)}")
print("\nCategories included in the plot:")
for i, (_, row) in enumerate(recent_data.iterrows()):
    print(f"{i+1}. {row['ExpenditureCategories']} - {row['CategoryName']}")