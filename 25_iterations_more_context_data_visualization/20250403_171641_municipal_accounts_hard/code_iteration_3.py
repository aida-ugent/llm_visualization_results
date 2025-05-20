# Automatically saved code from agent execution
# Run ID: 20250403_171641_municipal_accounts_hard, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/municipal_accounts.csv')

# Filter for the specific balance sheet items we're interested in
target_items = ['A12a - Other tangible fixed assets', 'A13 - Financial fixed assets']
target_regions = ['Noord-Nederland (LD)', 'Oost-Nederland (LD)', 'West-Nederland (LD)', 'Zuid-Nederland (LD)']
target_years = list(range(2015, 2023))  # 2015-2022

# Filter the dataframe
filtered_df = df[
    df['BalanceSheetItemsMunicipalities'].isin(target_items) & 
    df['Regions'].isin(target_regions) & 
    df['Periods'].isin(target_years)
]

# Check if we have data
if filtered_df.empty:
    print("No data found for the specified criteria. Checking available values...")
    print("\nAvailable balance sheet items:")
    print(df['BalanceSheetItemsMunicipalities'].unique())
    print("\nAvailable regions:")
    print(df['Regions'].unique())
    print("\nAvailable periods:")
    print(sorted(df['Periods'].unique()))
else:
    print(f"Found {len(filtered_df)} matching records")
    print(filtered_df.head())

# Set up the plot
plt.figure(figsize=(14, 10))
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_171641_municipal_accounts_hard/visualization.png')