# Automatically saved code from agent execution
# Run ID: 20250403_170248_consumer_prices_hard, Iteration: 4

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Filter for "All items" category
all_items_df = df[df['ExpenditureCategories'] == '000000 All items'].copy()

# Extract year and month from the Periods column
all_items_df['Year'] = all_items_df['Periods'].str.extract(r'(\d{4})').astype(int)
all_items_df['Month'] = all_items_df['Periods'].str.extract(r'\d{4}\s+(\w+)')

# Create a proper date column for better plotting
month_map = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}
all_items_df['Month_Num'] = all_items_df['Month'].map(month_map)

# Create date strings and convert to datetime
all_items_df['DateStr'] = all_items_df['Year'].astype(str) + '-' + all_items_df['Month_Num'].astype(str) + '-01'
all_items_df['Date'] = pd.to_datetime(all_items_df['DateStr'])

# Sort by date
all_items_df = all_items_df.sort_values('Date')

# Create the figure and axis
plt.figure(figsize=(12, 6))

# Plot the Derived CPI (excluding tax changes)
plt.plot(all_items_df['Date'], all_items_df['DerivedCPI_2'], linewidth=2, color='#1f77b4')

# Add annual markers for better readability
annual_data = all_items_df[all_items_df['Month'] == 'January'].copy()
plt.scatter(annual_data['Date'], annual_data['DerivedCPI_2'], color='#1f77b4', s=50, zorder=5)

# Set title and labels
plt.title('Consumer Price Index (Excluding Tax Changes) for All Items\n1996-Present', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12, labelpad=10)
plt.ylabel('Derived CPI (2015=100)', fontsize=12, labelpad=10)

# Format the x-axis to show years
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=45)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add annotations
min_year = all_items_df['Year'].min()
max_year = all_items_df['Year'].max()
plt.figtext(0.5, 0.01, f"Period: {min_year}-{max_year}. Derived CPI excludes the effect of changes in product-related taxes and subsidies.", 
            ha='center', fontsize=10, style='italic')

# Improve layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170248_consumer_prices_hard/visualization.png', dpi=300, bbox_inches='tight')

# Close the plot
plt.close()