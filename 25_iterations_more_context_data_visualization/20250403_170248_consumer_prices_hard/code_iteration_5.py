# Automatically saved code from agent execution
# Run ID: 20250403_170248_consumer_prices_hard, Iteration: 5

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

# Extract year from the Periods column
all_items_df['Year'] = all_items_df['Periods'].str.extract(r'(\d{4})').astype(int)

# For simplicity, let's use the annual average data
annual_data = all_items_df[all_items_df['Periods'].str.contains(r'^\d{4}$')].copy()

# If there's no annual data, let's create it by averaging the monthly data
if len(annual_data) == 0:
    # Group by year and calculate the mean of DerivedCPI_2
    annual_data = all_items_df.groupby('Year')['DerivedCPI_2'].mean().reset_index()
else:
    annual_data = annual_data[['Year', 'DerivedCPI_2']]

# Sort by year
annual_data = annual_data.sort_values('Year')

# Create the figure and axis
plt.figure(figsize=(12, 6))

# Plot the Derived CPI (excluding tax changes)
plt.plot(annual_data['Year'], annual_data['DerivedCPI_2'], linewidth=2, color='#1f77b4', marker='o')

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
min_year = annual_data['Year'].min()
max_year = annual_data['Year'].max()
plt.figtext(0.5, 0.01, f"Period: {min_year}-{max_year}. Derived CPI excludes the effect of changes in product-related taxes and subsidies.", 
            ha='center', fontsize=10, style='italic')

# Improve layout
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170248_consumer_prices_hard/visualization.png', dpi=300, bbox_inches='tight')

# Close the plot
plt.close()