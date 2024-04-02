# UK Deprivation Annual Index

This project generates vector tiles for the UK Deprivation Annual Index at the Lower Layer Super Output Area (LSOA) level.

## Data Sources

-   [Lower Layer Super Output Areas (December 2011) boundaries](02e8d336d6804fbeabe6c972e5a27b16)
-   [Annual Deprivation Index data](https://www.annualdeprivationindex.co.uk/)

## Processing Steps

1. Reproject LSOA boundary geometries to WGS84 with 6 decimal places precision
2. Run `process.py` to join the deprivation data to the LSOA boundaries
3. Generate vector tiles from the combined GeoJSON using tippecanoe:

```bash
tippecanoe --output=output/LSOA.pmtiles --generate-ids --force --no-feature-limit --no-tile-size-limit --detect-shared-borders --coalesce-fraction-as-needed --coalesce-densest-as-needed --coalesce-smallest-as-needed --coalesce --reorder --minimum-zoom=0 --maximum-zoom=17 -x FID -x LSOA11CD -x LSOA11NM -x LSOA11NMW -x BNG_E -x BNG_N -x LONG -x LAT -r1 output/LSOA.geojson
```

## Output

The final vector tileset is written to `output/LSOA.pmtiles`.
