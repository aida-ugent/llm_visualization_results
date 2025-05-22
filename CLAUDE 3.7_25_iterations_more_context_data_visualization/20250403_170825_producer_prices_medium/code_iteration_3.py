# Automatically saved code from agent execution
# Run ID: 20250403_170825_producer_prices_medium, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime

# Set the style for the plot
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/ppi.csv')

# Filter for 'B Mining and quarrying'
mining_data = df[df['ProductsAccordingToPRODCOMList'] == 'B Mining and quarrying']

# Convert the 'Periods' column to datetime for better plotting
def convert_period_to_date(period_str):
    month_dict = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    parts = period_str.split()
    year = int(parts[0])
    month = month_dict[parts[1]] if len(parts) > 1 else 1
    
    return datetime(year, month, 1)

# Apply the conversion
mining_data['Date'] = mining_data['Periods'].apply(convert_period_to_date)

# Sort by date to ensure proper chronological order
mining_data = mining_data.sort_values('Date')

# Create the figure and axis
plt.figure(figsize=(12, 6))

# Plot the month-on-month development
plt.plot(mining_data['Date'], mining_data['MonthOnMonthDevelopment_2'], 
         marker='o', markersize=3, linewidth=1.5, color='#1f77b4')

# Set the title and labels
plt.title('Month-on-Month Development for B Mining and Quarrying (2012-2023)', 
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Year', fontsize=12, labelpad=10)
plt.ylabel('Month-on-Month Development (%)', fontsize=12, labelpad=10)

# Format the x-axis to show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())

# Add a horizontal line at y=0 to highlight positive vs negative changes
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.7)

# Add grid for better readability
plt.grid(True, alpha=0.3)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Tight layout to ensure everything fits
plt.tight_layout()

# Add annotations for significant peaks and troughs
# Find the top 3 highest and lowest points
top_3_high = mining_data.nlargest(3, 'MonthOnMonthDevelopment_2')
top_3_low = mining_data.nsmallest(3, 'MonthOnMonthDevelopment_2')

# Annotate these points
for _, row in pd.concat([top_3_high, top_3_low]).iterrows():
    plt.annotate(f"{row['MonthOnMonthDevelopment_2']:.1f}%",
                 xy=(row['Date'], row['MonthOnMonthDevelopment_2']),
                 xytext=(0, 10 if row['MonthOnMonthDevelopment_2'] > 0 else -20),
                 textcoords='offset points',
                 ha='center',
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170825_producer_prices_medium/visualization.png', dpi=300, bbox_inches='tight')