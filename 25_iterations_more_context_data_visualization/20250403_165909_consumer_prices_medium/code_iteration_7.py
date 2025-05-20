# Automatically saved code from agent execution
# Run ID: 20250403_165909_consumer_prices_medium, Iteration: 7

import pandas as pd
import re

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/consumer_prices.csv')

# Examine the structure of the expenditure categories
print("Sample of ExpenditureCategories:")
print(df['ExpenditureCategories'].head(20))

# Let's identify the main categories (likely those with specific patterns)
# First, let's see how many digits are in the codes
df['code_length'] = df['ExpenditureCategories'].str.extract(r'(\d+)')[0].str.len()
print("\nDistribution of code lengths:")
print(df['code_length'].value_counts())

# Let's look at some examples of each code length
print("\nExamples of different code lengths:")
for length in sorted(df['code_length'].unique()):
    examples = df[df['code_length'] == length]['ExpenditureCategories'].unique()[:3]
    print(f"\nCode length {length} examples:")
    for ex in examples:
        print(f"  {ex}")

# Let's try to identify main categories (likely 2-digit codes followed by zeros)
pattern = r'^\d{2}0000\s'
main_cats = df[df['ExpenditureCategories'].str.match(pattern)]
print(f"\nNumber of main categories (matching pattern {pattern}): {len(main_cats['ExpenditureCategories'].unique())}")
print("Main categories:")
for cat in sorted(main_cats['ExpenditureCategories'].unique()):
    print(f"  {cat}")

# Let's also try to identify second-level categories
pattern2 = r'^\d{4}00\s'
second_level = df[df['ExpenditureCategories'].str.match(pattern2) & ~df['ExpenditureCategories'].str.match(pattern)]
print(f"\nNumber of second-level categories: {len(second_level['ExpenditureCategories'].unique())}")
print("Sample of second-level categories:")
for cat in sorted(second_level['ExpenditureCategories'].unique())[:10]:
    print(f"  {cat}")