import os
import json
import csv

# Set the paths to the input and output folders
input_folder = "data/ADI_all-domains"
output_folder = "output"

# Load the LSOA GeoJSON file
print("Loading LSOA GeoJSON file...")
with open("data/LSOA_WGS84.geojson") as f:
    lsoa_geojson = json.load(f)

# Create a dictionary to store the LSOA features by their code
lsoa_features = {
    feature["properties"]["LSOA11CD"]: feature for feature in lsoa_geojson["features"]
}

# Create a set to keep track of the LSOAs with matching data
matched_lsoas = set()

# Iterate over each year folder in ADI_all-domains
for year_folder in os.listdir(input_folder):
    if year_folder.startswith("."):
        continue
    year = year_folder.split("_")[-1]
    print(f"Processing data for year {year}...")

    # Load the CSV files for the current year
    csv_files = {
        "claimant_counts": f"ADI_claimant_counts_{year}.csv",
        "crime": f"ADI_crime_{year}.csv",
        "health": f"ADI_health_{year}.csv",
    }

    for data_type, csv_file in csv_files.items():
        csv_path = os.path.join(input_folder, year_folder, csv_file)
        print(f"Loading {data_type} data from {csv_path}")

        with open(csv_path) as f:
            csv_data = csv.DictReader(f)
            for row in csv_data:
                lsoa_code = row["area_code"]
                if lsoa_code in lsoa_features:
                    matched_lsoas.add(lsoa_code)
                    for key, value in row.items():
                        if key != "area_code" and key != "area_name":
                            if value:
                                try:
                                    value = float(value)
                                    value = f"{value:.2f}"
                                except ValueError:
                                    pass
                                lsoa_features[lsoa_code]["properties"][
                                    f"{key}_{year}"
                                ] = value

# Remove the LSOA features that don't have matching data
lsoa_geojson["features"] = [lsoa_features[lsoa_code] for lsoa_code in matched_lsoas]

# Save the updated LSOA GeoJSON to the output folder
output_file = os.path.join(output_folder, "LSOA.geojson")
print(f"Saving updated LSOA GeoJSON to {output_file}")
with open(output_file, "w") as f:
    json.dump(lsoa_geojson, f, indent=2)
