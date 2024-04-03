import pandas as pd
import os

# Define the input file paths
claimant_file = "data/ADI_all-domains/ADI_2013/ADI_claimant_counts_2013.csv"
crime_file = "data/ADI_all-domains/ADI_2013/ADI_crime_2013.csv"
health_file = "data/ADI_all-domains/ADI_2013/ADI_health_2013.csv"

# Load the data into DataFrames
claimant_df = pd.read_csv(claimant_file)
crime_df = pd.read_csv(crime_file)
health_df = pd.read_csv(health_file)

# Combine the DataFrames
combined_df = pd.concat([claimant_df, crime_df, health_df], axis=1)

# Get all columns ending with "_rate"
rate_columns = [col for col in combined_df.columns if col.endswith("_rate")]

# Calculate the mean and standard deviation for each rate column
results = {}
for col in rate_columns:
    mean = combined_df[col].mean()
    std = combined_df[col].std()
    min_value = mean - 2 * std
    max_value = mean + 2 * std
    results[col] = {"min": min_value, "max": max_value}

# Write the results to a file
output_file = "output/2013_rate_ranges.txt"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w") as file:
    for col, values in results.items():
        file.write(f"{col}:\n")
        file.write(f"  Min: {values['min']}\n")
        file.write(f"  Max: {values['max']}\n")
        file.write("\n")

print(f"Results written to {output_file}")
