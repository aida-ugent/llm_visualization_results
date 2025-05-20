# Automatically saved code from agent execution
# Run ID: 20250403_165609_consumer_prices_easy, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Set the style for the plot
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Filter for "All items" category
all_items_df = df[df['ExpenditureCategories'] == '000000 All items']

# Convert the Periods column to datetime
all_items_df['Date'] = pd.to_datetime(all_items_df['Periods'], format='%Y %B', errors='coerce')

# Sort by date to ensure proper chronological order
all_items_df = all_items_df.sort_values('Date')

# Plot the CPI over time
plt.plot(all_items_df['Date'], all_items_df['CPI_1'], linewidth=2, color='#1f77b4')

# Add title and labels
plt.title('Consumer Price Index (CPI) for All Items Over Time', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Consumer Price Index (CPI)', fontsize=12)

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))  # Show every 2 years
plt.xticks(rotation=45)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add a note about the data source
plt.figtext(0.5, 0.01, 'Source: Dutch Consumer Price Index (CPI) Data', 
            ha='center', fontsize=10, style='italic')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_165609_consumer_prices_easy/visualization.png', dpi=300, bbox_inches='tight')