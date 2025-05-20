# Automatically saved code from agent execution
# Run ID: 20250403_171413_municipal_accounts_easy, Iteration: 5

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style
sns.set_style("whitegrid")
plt.figure(figsize=(12, 8))

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/municipal_accounts.csv')

# Filter for Netherlands data and main balance sheet categories
main_categories = ['A - Assets', 'A1 - Fixed assets', 'A11 - Intangible assets', 
                  'A12 - Tangible fixed assets', 'A13 - Financial fixed assets']
filtered_df = df[(df['Regions'] == 'The Netherlands') & 
                (df['BalanceSheetItemsMunicipalities'].isin(main_categories))]

# Pivot the data for plotting
pivot_df = filtered_df.pivot(index='Periods', 
                            columns='BalanceSheetItemsMunicipalities', 
                            values='BalanceSheetItemsYearEndInMlnEuro_1')

# Plot the data
ax = pivot_df.plot(kind='line', marker='o', linewidth=2.5, markersize=6)

# Customize the plot
plt.title('Balance Sheet Items Year-End Values Over Time in the Netherlands', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Value (Million Euro)', fontsize=14)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add legend with better positioning
plt.legend(title='Balance Sheet Items', title_fontsize=12, fontsize=10, 
           bbox_to_anchor=(1.05, 1), loc='upper left')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the plot
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_171413_municipal_accounts_easy/visualization.png', 
            dpi=300, bbox_inches='tight')