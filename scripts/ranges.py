import pandas as pd
import os

# Define the input file paths for each year
years = range(2013, 2023)
file_paths = {}
for year in years:
    file_paths[year] = {
        "claimant": f"data/ADI_all-domains/ADI_{year}/ADI_claimant_counts_{year}.csv",
        "crime": f"data/ADI_all-domains/ADI_{year}/ADI_crime_{year}.csv",
        "health": f"data/ADI_all-domains/ADI_{year}/ADI_health_{year}.csv",
    }

# Initialize variables to store the results and earliest year for each column
results = {}
earliest_year = {}

# Process each year
for year in years:
    try:
        # Load the data into DataFrames
        claimant_df = pd.read_csv(file_paths[year]["claimant"])
        crime_df = pd.read_csv(file_paths[year]["crime"])
        health_df = pd.read_csv(file_paths[year]["health"])

        # Combine the DataFrames
        combined_df = pd.concat([claimant_df, crime_df, health_df], axis=1)

        # Get all columns ending with "_rate"
        rate_columns = [col for col in combined_df.columns if col.endswith("_rate")]

        # Update the results and earliest year for each column
        for col in rate_columns:
            mean = combined_df[col].mean()
            std = combined_df[col].std()
            min_value = mean - 2 * std
            max_value = mean + 2 * std

            if col not in results:
                results[col] = {"min": min_value, "max": max_value}
                earliest_year[col] = year
            else:
                results[col]["min"] = min(results[col]["min"], min_value)
                results[col]["max"] = max(results[col]["max"], max_value)

    except FileNotFoundError:
        print(f"Skipping year {year} due to missing file(s).")

# Add the earliest year to the results dictionary
for col in results:
    results[col]["earliest_year"] = earliest_year[col]

# Write the results to a file
output_file = "output/rate_ranges.txt"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w") as file:
    for col, values in results.items():
        file.write(f"{col} (earliest year: {values['earliest_year']}):\n")
        file.write(f"  Min: {values['min']}\n")
        file.write(f"  Max: {values['max']}\n")
        file.write("\n")

print(f"Results written to {output_file}")
