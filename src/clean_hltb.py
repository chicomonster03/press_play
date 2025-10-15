import pandas as pd

# === Configuration ===
INPUT_CSV = "docs/howlongtobeat.csv"                      # your raw input
OUTPUT_CSV = "docs/hltb_cleaned_with_genre.csv"         # your desired output

# === Genre exclusions and logic ===
EXCLUDED = {
    "First-Person", "Third-Person", "Side", "Scrolling", "Open World"
}

MERGE_MAP = {
    "Survival Horror": "Horror",
    "Horror": "Horror"
}

GENRE_PRIORITY = ["RPG", "Horror", "Adventure", "Shooter", "Action", "Platform", "Puzzle"]

# === Genre Extraction Function ===
def extract_primary_genre(genre_str):
    if pd.isna(genre_str):
        return None
    try:
        genre_list = [g.strip() for g in genre_str.split(",")]
        cleaned = [MERGE_MAP.get(g, g) for g in genre_list if g not in EXCLUDED]
        for p in GENRE_PRIORITY:
            if p in cleaned:
                return p
        return cleaned[0] if cleaned else None
    except:
        return None

# === Load, clean, and save ===
df = pd.read_csv(INPUT_CSV)

df["Primary_Genre"] = df["Genres"].apply(extract_primary_genre)

df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Cleaned file written to: {OUTPUT_CSV}")