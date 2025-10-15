import json
import csv
import re
from datetime import datetime

def time_to_hours(time_str):
    """Convert strings like '18h 30m' or '45m' into float hours."""
    if not time_str or time_str.strip() in ["--", ""]:
        return None
    time_str = time_str.lower().replace("hours", "h").replace("hour", "h")
    h, m = 0, 0
    # Match hours
    h_match = re.search(r'(\d+)\s*h', time_str)
    if h_match:
        h = int(h_match.group(1))
    # Match minutes
    m_match = re.search(r'(\d+)\s*m', time_str)
    if m_match:
        m = int(m_match.group(1))
    return round(h + m / 60, 2)

def extract_times(stats):
    """Extract single-player average times."""
    time_data = {}
    keys = ["Main Story", "Main + Extras", "Completionist", "All PlayStyles"]
    for key in keys:
        section = stats.get("Single-Player", {}).get(key, {})
        avg_time = section.get("Average", "")
        time_data[f"Avg_{key.replace(' ', '_')}"] = time_to_hours(avg_time)
    return time_data

def extract_speedrun(stats):
    """Extract speedrun times if available."""
    sr_data = {}
    anypercent = stats.get("Speedruns", {}).get("Any%", {})
    sr_data["Speedrun_Avg"] = time_to_hours(anypercent.get("Average", ""))
    sr_data["Speedrun_Fastest"] = time_to_hours(anypercent.get("Fastest", ""))
    sr_data["Speedrun_Slowest"] = time_to_hours(anypercent.get("Slowest", ""))
    return sr_data

# Change these file names to your actual paths
input_path = "data/hltb.jsonlines"
output_path = "docs/howlongtobeat.csv"

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", newline="", encoding="utf-8") as outfile:
    fieldnames = [
        "Name", "Release_Year", "Genres", "Review_Score",
        "Avg_Main_Story", "Avg_Main_+_Extras", "Avg_Completionist", "Avg_All_PlayStyles",
        "Speedrun_Avg", "Speedrun_Fastest", "Speedrun_Slowest"
    ]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for line in infile:
        record = json.loads(line)
        name = record.get("Name")
        release_date = record.get("Release_date", "")
        year = ""
        try:
            year = datetime.strptime(release_date, "%Y-%m-%d").year
        except:
            pass

        flat_row = {
            "Name": name,
            "Release_Year": year,
            "Genres": record.get("Genres", ""),
            "Review_Score": record.get("Review_score", "")
        }
        # add main times
        flat_row.update(extract_times(record.get("Stats", {})))
        # add speedrun times
        flat_row.update(extract_speedrun(record.get("Stats", {})))

        writer.writerow(flat_row)

print(f"✅ Flattened data with speedrun stats saved to: {output_path}")