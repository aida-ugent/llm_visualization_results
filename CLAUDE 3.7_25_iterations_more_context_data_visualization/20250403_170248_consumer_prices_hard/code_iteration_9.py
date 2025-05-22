# Automatically saved code from agent execution
# Run ID: 20250403_170248_consumer_prices_hard, Iteration: 9

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import MaxNLocator

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

# Calculate year-on-year percentage change
annual_data['YoY_Change'] = annual_data['DerivedCPI_2'].pct_change() * 100

# Create the figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

# Plot 1: Derived CPI (excluding tax changes)
ax1.plot(annual_data['Year'], annual_data['DerivedCPI_2'], linewidth=2.5, color='#1f77b4', marker='o', markersize=6)

# Add reference line for 2015=100 (base year)
ax1.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Base Year (2015=100)')

# Highlight the recent inflation period (2020-2023)
recent_years = annual_data[annual_data['Year'] >= 2020].copy()
ax1.plot(recent_years['Year'], recent_years['DerivedCPI_2'], linewidth=3.5, color='#ff7f0e', marker='o', markersize=8, label='Recent Inflation Period')

# Set title and labels for first plot
ax1.set_title('Consumer Price Index (Excluding Tax Changes) for All Items\n1996-Present', fontsize=16, pad=20)
ax1.set_ylabel('Derived CPI (2015=100)', fontsize=12, labelpad=10)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(loc='upper left')

# Annotate important points
# Find the maximum CPI value and its year
max_cpi_idx = annual_data['DerivedCPI_2'].idxmax()
max_cpi_year = annual_data.loc[max_cpi_idx, 'Year']
max_cpi_value = annual_data.loc[max_cpi_idx, 'DerivedCPI_2']

# Annotate the maximum point
ax1.annotate(f'Latest: {max_cpi_value:.1f}',
             xy=(max_cpi_year, max_cpi_value),
             xytext=(max_cpi_year-2, max_cpi_value+3),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=10)

# Plot 2: Year-on-Year percentage change
bars = ax2.bar(annual_data['Year'][1:], annual_data['YoY_Change'][1:], color='#1f77b4', alpha=0.7)

# Color the bars based on positive/negative values
for i, bar in enumerate(bars):
    if annual_data['YoY_Change'].iloc[i+1] < 0:
        bar.set_color('#d62728')  # Red for negative
    else:
        bar.set_color('#2ca02c')  # Green for positive

# Highlight the recent inflation spike
recent_years_idx = annual_data[annual_data['Year'] >= 2020].index
for i in recent_years_idx:
    if i > 0:  # Skip the first year as it has no YoY change
        idx = i - annual_data.index[0] - 1  # Adjust index for the bars
        if idx < len(bars):
            bars[idx].set_color('#ff7f0e')
            bars[idx].set_alpha(1.0)
            # Add value label for recent years
            ax2.annotate(f"{annual_data['YoY_Change'].iloc[i]:.1f}%",
                        xy=(annual_data['Year'].iloc[i], annual_data['YoY_Change'].iloc[i]),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', fontsize=9, fontweight='bold')

# Add a horizontal line at y=0
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

# Set labels for second plot
ax2.set_xlabel('Year', fontsize=12, labelpad=10)
ax2.set_ylabel('Year-on-Year Change (%)', fontsize=12, labelpad=10)
ax2.grid(True, linestyle='--', alpha=0.7)

# Format the x-axis to show years
ax2.xaxis.set_major_locator(MaxNLocator(20))
plt.xticks(rotation=45)

# Add annotations
min_year = annual_data['Year'].min()
max_year = annual_data['Year'].max()
plt.figtext(0.5, 0.01, 
            f"Period: {min_year}-{max_year}. Derived CPI excludes the effect of changes in product-related taxes and subsidies.\nNote the significant inflation spike in 2022 (11.8%).", 
            ha='center', fontsize=10, style='italic')

# Improve layout
plt.tight_layout()
plt.subplots_adjust(bottom=0.08)

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_170248_consumer_prices_hard/visualization.png', dpi=300, bbox_inches='tight')

# Close the plot
plt.close()