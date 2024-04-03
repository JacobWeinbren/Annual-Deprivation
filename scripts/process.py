import os
import ujson
import csv
from collections import defaultdict

# Set the paths to the input and output folders
input_folder = "data/ADI_all-domains"
output_folder = "output"

# Load the LSOA GeoJSON file
print("Loading LSOA GeoJSON file...")
with open("data/LSOA_WGS84.geojson") as f:
    lsoa_geojson = ujson.load(f)

# Create a dictionary to store the LSOA features by their code
lsoa_features = {
    feature["properties"]["LSOA11CD"]: feature for feature in lsoa_geojson["features"]
}

# Iterate over each year folder in ADI_all-domains
for year_folder in [f for f in os.listdir(input_folder) if not f.startswith(".")]:
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

        # Read the CSV file and process each row
        with open(csv_path) as f:
            csv_reader = csv.reader(f)
            headers = next(csv_reader)

            for row in csv_reader:
                lsoa_code = row[headers.index("area_code")]

                if lsoa_code in lsoa_features:
                    feature = lsoa_features[lsoa_code]
                    for key, value in zip(headers, row):
                        if key.endswith("_rate") and value:
                            try:
                                value = float(value)
                                feature["properties"][f"{key}_{year}"] = round(value, 2)
                            except ValueError:
                                continue

# Get the unique variable names
variable_names = set()
for feature in lsoa_features.values():
    for key in feature["properties"]:
        if "_" in key:
            variable_name, _ = key.rsplit("_", 1)
            variable_names.add(variable_name)

# Create and write the GeoJSON files for each variable
for variable_name in variable_names:
    output_geojson = {"type": "FeatureCollection", "features": []}

    for lsoa_code, feature in lsoa_features.items():
        output_feature = {
            "type": "Feature",
            "geometry": feature["geometry"],
            "properties": {"LSOA11CD": lsoa_code},
        }

        for key, value in feature["properties"].items():
            if key.startswith(variable_name):
                output_feature["properties"][key] = value

        output_geojson["features"].append(output_feature)

    output_file = os.path.join(output_folder, f"{variable_name}.geojson")
    with open(output_file, "w") as f:
        ujson.dump(output_geojson, f, indent=2)

print("Processing complete.")
