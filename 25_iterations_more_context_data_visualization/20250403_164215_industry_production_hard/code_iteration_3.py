# Automatically saved code from agent execution
# Run ID: 20250403_164215_industry_production_hard, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/alexanderrogiers/ugent/llm_visualization/data/industry_sales.csv')

# Check unique sectors to confirm if '16 Manufacture of wood products' exists
unique_sectors = df['SectorBranchesSIC2008'].unique()
print("Number of unique sectors:", len(unique_sectors))
print("First 10 sectors:")
for sector in unique_sectors[:10]:
    print(f"- {sector}")

# Check if our target sector exists
target_sector = '16 Manufacture of wood products'
exists = target_sector in unique_sectors
print(f"\nDoes '{target_sector}' exist in the dataset? {exists}")

# If it doesn't exist exactly as specified, look for similar sectors
if not exists:
    similar_sectors = [s for s in unique_sectors if 'wood' in s.lower()]
    print("\nSimilar sectors containing 'wood':")
    for sector in similar_sectors:
        print(f"- {sector}")

# Just to create a placeholder visualization
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, "This is a placeholder - checking data structure", 
         ha='center', va='center', fontsize=12)
plt.axis('off')
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_164215_industry_production_hard/visualization.png')