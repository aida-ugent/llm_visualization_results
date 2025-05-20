# Automatically saved code from agent execution
# Run ID: 20250403_164937_milk_supply_hard, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

# Load the data
file_path = '/Users/alexanderrogiers/ugent/llm_visualization/data/milk_production_1.csv'
df = pd.read_csv(file_path)

# Extract year from the 'Periods' column
df['Year'] = df['Periods'].str.extract(r'(\d{4})').astype(int)

# Get the current year to determine the last 5 years
current_year = datetime.now().year

# Filter for the last 5 years of data (assuming the data is up to date)
# Find the 5 most recent years in the dataset
unique_years = sorted(df['Year'].unique(), reverse=True)
last_5_years = unique_years[:5]

# Filter the dataframe for these years
df_recent = df[df['Year'].isin(last_5_years)]

# For yearly data, filter rows that contain only the year (annual totals)
df_yearly = df_recent[df_recent['Periods'].str.match(r'^\d{4}$')]

# If no yearly data is available, aggregate monthly data
if len(df_yearly) < 5:
    # Group by year and sum the production volumes
    df_yearly = df_recent.groupby('Year').agg({
        'Butter_4': 'sum',
        'Cheese_5': 'sum',
        'TotalMilkPowder_6': 'sum',
        'WholeMilkPowder_7': 'sum',
        'SkimmedMilkPowder_8': 'sum',
        'ConcentratedMilk_9': 'sum',
        'WheyPowder_10': 'sum'
    }).reset_index()

# Select the columns for dairy products
dairy_products = ['Butter_4', 'Cheese_5', 'TotalMilkPowder_6', 
                  'WholeMilkPowder_7', 'SkimmedMilkPowder_8', 
                  'ConcentratedMilk_9', 'WheyPowder_10']

# Create a more readable mapping for the column names
product_names = {
    'Butter_4': 'Butter',
    'Cheese_5': 'Cheese',
    'TotalMilkPowder_6': 'Total Milk Powder',
    'WholeMilkPowder_7': 'Whole Milk Powder',
    'SkimmedMilkPowder_8': 'Skimmed Milk Powder',
    'ConcentratedMilk_9': 'Concentrated Milk',
    'WheyPowder_10': 'Whey Powder'
}

# Melt the dataframe for easier plotting
df_melted = pd.melt(df_yearly, 
                    id_vars=['Year'], 
                    value_vars=dairy_products,
                    var_name='Product', 
                    value_name='Production Volume')

# Replace the product codes with readable names
df_melted['Product'] = df_melted['Product'].map(product_names)

# Set up the figure with a larger size for better readability
plt.figure(figsize=(14, 8))

# Create a grouped bar chart
sns.barplot(x='Year', y='Production Volume', hue='Product', data=df_melted)

# Add title and labels
plt.title('Production Volume of Dairy Products in the Netherlands (Last 5 Years)', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Production Volume', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Add a legend with a better position
plt.legend(title='Dairy Product', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

# Add grid lines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the figure
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164937_milk_supply_hard/visualization.png', dpi=300, bbox_inches='tight')

# Show the plot (this won't be visible in the execution environment but is good practice)
plt.close()