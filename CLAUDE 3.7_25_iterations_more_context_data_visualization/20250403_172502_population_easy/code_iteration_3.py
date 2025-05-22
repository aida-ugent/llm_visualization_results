# Automatically saved code from agent execution
# Run ID: 20250403_172502_population_easy, Iteration: 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the plot
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Load the data
data_path = '/Users/alexanderrogiers/ugent/llm_visualization/data/population.csv'
df = pd.read_csv(data_path)

# Filter for total population only (all rows where all demographic variables are "Total")
total_pop = df[(df['Sex'] == 'Total males and females') & 
               (df['Age'] == 'Total') & 
               (df['MaritalStatus'] == 'Total') & 
               (df['Generation'] == 'Total') & 
               (df['MigrationBackground'] == 'Total')]

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Plot the data
ax.plot(total_pop['Periods'], total_pop['Population_1'] / 1000000, 
        marker='o', linewidth=2, markersize=6)

# Add labels and title
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Population (millions)', fontsize=12)
ax.set_title('Total Population in the Netherlands (1996-2022)', fontsize=16, pad=20)

# Format the y-axis to show millions with 1 decimal place
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}'))

# Add grid lines for better readability
ax.grid(True, linestyle='--', alpha=0.7)

# Annotate the start and end points
start_year = total_pop['Periods'].iloc[0]
start_pop = total_pop['Population_1'].iloc[0] / 1000000
end_year = total_pop['Periods'].iloc[-1]
end_pop = total_pop['Population_1'].iloc[-1] / 1000000

ax.annotate(f'{start_pop:.2f}M', 
            xy=(start_year, start_pop),
            xytext=(start_year-1, start_pop-0.2),
            fontsize=10)

ax.annotate(f'{end_pop:.2f}M', 
            xy=(end_year, end_pop),
            xytext=(end_year-1, end_pop+0.2),
            fontsize=10)

# Add a text box with key statistics
growth = ((end_pop - start_pop) / start_pop) * 100
avg_annual_growth = growth / (end_year - start_year)
textstr = f'Population Growth (1996-2022):\n{growth:.1f}% total\n{avg_annual_growth:.2f}% annual average'
props = dict(boxstyle='round', facecolor='white', alpha=0.7)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('/Users/alexanderrogiers/ugent/llm_visualization/output/20250403_172502_population_easy/visualization.png', dpi=300)
plt.close()