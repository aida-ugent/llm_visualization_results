# Automatically saved code from agent execution
# Run ID: 20250403_170512_producer_prices_easy, Iteration: 5

import pandas as pd

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/ppi.csv')

# Check unique values in the Periods column
unique_periods = df['Periods'].unique()
print("Number of unique periods:", len(unique_periods))
print("Sample of unique periods:")
print(unique_periods[:20])  # Print first 20 unique periods

# Check if there are any periods that don't follow the expected format
# Expected format: "YYYY Month"
import re
pattern = re.compile(r'^\d{4} [A-Za-z]+$')
non_standard_periods = [period for period in unique_periods if not pattern.match(period)]
print("\nNon-standard periods:")
print(non_standard_periods)

# Check if there are any annual periods
annual_periods = [period for period in unique_periods if 'year' in period.lower()]
print("\nAnnual periods:")
print(annual_periods)