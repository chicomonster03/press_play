import json
import pandas as pd
import re
from pathlib import Path

# Convert time strings like "23h 17m" or "1h 30m" to minutes
def time_to_minutes(t_str):
    if not t_str or t_str == "--":
        return None
    t_str = t_str.strip().lower().replace("hours", "h").replace("hour", "h")
    t_str = re.sub(r"(\d+)\s*½", lambda m: str(float(m.group(1)) + 0.5), t_str)
    t_str = re.sub(r"½", "0.5", t_str)

    h, m = 0, 0
    matches = re.findall(r"(\d+(?:\.\d+)?)(h|m)", t_str)
    for val, unit in matches:
        if unit == "h":
            h += float(val)
        elif unit == "m":
            m += float(val)
    return round(h * 60 + m)

# Load JSON lines (one record per line)
def load_hltb_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

# Extract relevant playtimes
def extract_times(game):
    stats = game.get("Stats", {})
    sp = stats.get("Single-Player", {})
    return {
        "Game": game.get("Name", "Unknown"),
        "MainStoryMins": time_to_minutes(sp.get("Main Story", {}).get("Average")),
        "CompletionistMins": time_to_minutes(sp.get("Completionist", {}).get("Average"))
    }

# Main process
def process_to_dumbbell(input_path, output_path):
    print("📥 Loading data...")
    data = load_hltb_jsonl(input_path)

    print(f"🔍 Processing {len(data)} games...")
    rows = [extract_times(game) for game in data]
    df = pd.DataFrame(rows).dropna(subset=["MainStoryMins", "CompletionistMins"])

    print(f"✅ {len(df)} games with valid times.")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"📄 Saved to {output_path}")

# Example
if __name__ == "__main__":
    process_to_dumbbell("data/hltb.jsonlines", "cleaned/hltb_dumbbell_data.csv")