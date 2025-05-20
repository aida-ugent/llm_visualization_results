# Automatically saved code from agent execution
# Run ID: 20250403_164705_milk_supply_medium, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

# Set the style for the plot
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

# Load the data
file_path = '/Users/alexanderrogiers/ugent/llm_visualization/data/milk_production_1.csv'
df = pd.read_csv(file_path)

# Convert the 'Periods' column to a datetime format
def parse_period(period):
    parts = period.split()
    if len(parts) == 2:
        year, month = parts
        # Convert month name to month number
        datetime_obj = datetime.strptime(f"{year} {month}", "%Y %B")
        return datetime_obj
    return None

# Apply the parsing function and create a new column
df['Date'] = df['Periods'].apply(parse_period)

# Filter for the years 2010-2015
mask = (df['Date'] >= datetime(2010, 1, 1)) & (df['Date'] <= datetime(2015, 12, 31))
filtered_df = df[mask].copy()

# Sort by date to ensure proper plotting
filtered_df = filtered_df.sort_values('Date')

# Plot the data
plt.plot(filtered_df['Date'], filtered_df['Volume_1'], marker='o', linestyle='-', color='#1f77b4', linewidth=1.5, markersize=4)

# Format the x-axis to show months and years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Show every 3 months
plt.gcf().autofmt_xdate()  # Rotate date labels

# Add labels and title
plt.title('Monthly Volume of Raw Cow\'s Milk Delivered by Dairy Farmers (2010-2015)', fontsize=14, pad=20)
plt.xlabel('Month', fontsize=12, labelpad=10)
plt.ylabel('Volume (in tons)', fontsize=12, labelpad=10)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add a subtle background color to enhance readability
plt.gca().set_facecolor('#f8f9fa')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164705_milk_supply_medium/visualization.png', dpi=300, bbox_inches='tight')

# Close the plot to free memory
plt.close()