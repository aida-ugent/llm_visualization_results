# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 13

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

# Let's try to get more categories by looking at level 3 categories
# First, let's see what level 3 categories are available
level3_cats = recent_data[recent_data['ExpenditureCategories'].str.match(level3_pattern) & 
                         ~recent_data['ExpenditureCategories'].str.match(level1_pattern) & 
                         ~recent_data['ExpenditureCategories'].str.match(level2_pattern)]

print(f"Number of level 3 categories in {most_recent_period}: {len(level3_cats)}")

# Let's combine level 2 and some level 3 categories
# First, get all level 2 categories
level2_recent = recent_data[recent_data['ExpenditureCategories'].str.match(level2_pattern) & 
                           ~recent_data['ExpenditureCategories'].str.match(level1_pattern)]

# Now, let's add some level 3 categories that are not subcategories of our level 2 categories
# We'll identify level 3 categories by their first 4 digits not matching any level 2 category
level2_prefixes = [cat.split()[0][:4] for cat in level2_recent['ExpenditureCategories']]

# Get level 3 categories that don't belong to our level 2 categories
additional_cats = []
for _, row in level3_cats.iterrows():
    cat_code = row['ExpenditureCategories'].split()[0]
    prefix = cat_code[:4]
    if prefix not in level2_prefixes:
        additional_cats.append(row)

additional_df = pd.DataFrame(additional_cats) if additional_cats else pd.DataFrame()

# Combine level 2 and additional level 3 categories
combined_cats = pd.concat([level2_recent, additional_df])

# Clean category names for display
combined_cats['CategoryName'] = combined_cats['ExpenditureCategories'].str.extract(r'\d{6}\s+(.*)')

# Sort by DerivedCPI value
combined_cats = combined_cats.sort_values('DerivedCPI_2', ascending=False)

# Limit to top 10 categories for better visualization
if len(combined_cats) > 10:
    combined_cats = combined_cats.head(10)

# Print the categories we'll be plotting
print(f"\nPlotting {len(combined_cats)} categories:")
for i, (_, row) in enumerate(combined_cats.iterrows()):
    print(f"{i+1}. {row['ExpenditureCategories']} - DerivedCPI: {row['DerivedCPI_2']}")

# Create the plot
plt.figure(figsize=(16, 10))
sns.set_style("whitegrid")

# Create the bar plot
ax = sns.barplot(
    x='CategoryName', 
    y='DerivedCPI_2', 
    data=combined_cats, 
    palette='viridis'
)

# Add labels and title
plt.title(f'Derived Consumer Price Index by Product Category\n(Period: {most_recent_period})', fontsize=16)
plt.xlabel('Product Category', fontsize=14)
plt.ylabel('Derived CPI', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Add data labels on top of bars
for i, v in enumerate(combined_cats['DerivedCPI_2']):
    ax.text(i, v + 1, f'{v:.1f}', ha='center', fontsize=9)

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165909_consumer_prices_medium/visualization.png', dpi=300, bbox_inches='tight')

print(f"\nVisualization saved with {len(combined_cats)} product categories.")