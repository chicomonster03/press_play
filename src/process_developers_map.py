import pandas as pd
import os
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
OUTPUT_PATH = "cleaned/dev_density_data.csv"
SAVE_EVERY_N = 10  # Save progress after every N successful geocodes
MAX_WORKERS = 5     # Be respectful of Nominatim's rate limits (no more than 1/sec globally)

# Step 1: Load and merge both datasets
print("📥 Loading datasets...")
main_df = pd.read_csv("data/video-games-developers.csv")
indie_df = pd.read_csv("data/indie-games-developers.csv")

# Align columns
indie_df = indie_df.rename(columns={"Autonomous area": "Administrative division"})
indie_df["Est."] = None
main_df["Type"] = "main"
indie_df["Type"] = "indie"

shared_cols = ["Developer", "City", "Administrative division", "Country", "Est.", "Type"]
main_df = main_df[shared_cols]
indie_df = indie_df[shared_cols]
combined = pd.concat([main_df, indie_df], ignore_index=True)

# Drop bad rows early
combined = combined.dropna(subset=["City", "Country"])
combined["Est."] = pd.to_numeric(combined["Est."], errors="coerce")

# Step 2: Aggregate by City + Country
print("📊 Grouping by city and country...")
grouped = combined.groupby(["City", "Country"]).agg(
    DevCount=("Developer", "count"),
    AvgFoundingYear=("Est.", "mean"),
    IndieCount=("Type", lambda x: (x == "indie").sum()),
    MainCount=("Type", lambda x: (x == "main").sum())
).reset_index()

# Add metrics
grouped["AvgFoundingYear"] = grouped["AvgFoundingYear"].round(1)
grouped["IndieRatio"] = grouped["IndieCount"] / grouped["DevCount"]

# Step 3: Resume if partial output exists
if os.path.exists(OUTPUT_PATH):
    print("🔁 Resuming from existing file...")
    saved = pd.read_csv(OUTPUT_PATH)
    grouped = grouped.merge(saved[["City", "Country", "Latitude", "Longitude"]], how="left", on=["City", "Country"])
else:
    grouped["Latitude"] = None
    grouped["Longitude"] = None

# Step 4: Setup geocoder
geolocator = Nominatim(user_agent="press_play_mapper", timeout=10)

def geocode_city(city, country):
    query = f"{city}, {country}"
    try:
        location = geolocator.geocode(query)
        if location:
            print(f"📍 {query} → ({location.latitude:.2f}, {location.longitude:.2f})")
            return (city, country, location.latitude, location.longitude)
        else:
            print(f"⚠️ {query} not found")
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"❌ Geocode failed: {query} — {e}")
    return (city, country, None, None)

# Step 5: Run geocoding in parallel
to_geocode = grouped[grouped["Latitude"].isnull()][["City", "Country"]].drop_duplicates()
print(f"🗺️ Starting geocoding for {len(to_geocode)} locations with {MAX_WORKERS} threads...")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(geocode_city, row.City, row.Country): (row.City, row.Country) for _, row in to_geocode.iterrows()}
    completed = 0

    for future in as_completed(futures):
        city, country, lat, lon = future.result()
        grouped.loc[(grouped["City"] == city) & (grouped["Country"] == country), ["Latitude", "Longitude"]] = [lat, lon]
        completed += 1

        # Save every N results
        if completed % SAVE_EVERY_N == 0:
            print(f"💾 Saving progress at {completed} completed geocodes...")
            grouped.dropna(subset=["Latitude", "Longitude"]).to_csv(OUTPUT_PATH, index=False)

# Final save
print("✅ Final save...")
grouped.dropna(subset=["Latitude", "Longitude"]).to_csv(OUTPUT_PATH, index=False)
print(f"🎉 Saved to {OUTPUT_PATH}")