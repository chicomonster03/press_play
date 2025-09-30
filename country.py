import pandas as pd

# Load the dataset
df = pd.read_csv("data/video-games-developers.csv")

# Drop rows with no country listed
df = df.dropna(subset=["Country"])

# Fix known mismatches between your CSV and the GeoJSON
country_renames = {
    "USA": "United States of America",
    "US": "United States of America",
    "UK": "United Kingdom",
    "Russia": "Russian Federation",
    "South Korea": "Republic of Korea",
    "North Korea": "Dem. Rep. Korea",
    "Iran": "Iran (Islamic Republic of)",
    "Syria": "Syrian Arab Republic",
    "Vietnam": "Viet Nam",
    "Venezuela": "Venezuela (Bolivarian Republic of)",
    "Czech Republic": "Czechia",
    "Macedonia": "North Macedonia",
    "Bolivia": "Bolivia (Plurinational State of)",
    "Moldova": "Republic of Moldova",
    "Tanzania": "United Republic of Tanzania",
    "Laos": "Lao People's Democratic Republic",
    "Ivory Coast": "Côte d'Ivoire"
}

df["Country"] = df["Country"].replace(country_renames)

# Strip whitespace in country names
df["Country"] = df["Country"].str.strip()

# Group by Country and count
country_counts = df["Country"].value_counts().reset_index()
country_counts.columns = ["Country", "CompanyCount"]

# Save the result
country_counts.to_csv("data/company_counts_by_country.csv", index=False)

print("✅ Done! File saved to: data/company_counts_by_country.csv")