import pandas as pd

# Load your data
df = pd.read_csv('cleaned/speedrun_country_agg.csv')

# Country centroids (approximate)
centroids = {
    'USA': (-95.7129, 37.0902),
    'GBR': (-3.4360, 55.3781),
    'DEU': (10.4515, 51.1657),
    'CAN': (-106.3468, 56.1304),
    'FRA': (2.2137, 46.2276),
    'JPN': (138.2529, 36.2048),
    'AUS': (133.7751, -25.2744),
    'SWE': (18.6435, 60.1282),
    'NLD': (5.2913, 52.1326),
    'BRA': (-51.9253, -14.2350),
    'POL': (19.1451, 51.9194),
    'ESP': (-3.7492, 40.4637),
    'ITA': (12.5674, 41.8719),
    'CHE': (8.2275, 46.8182),
    'FIN': (25.7482, 61.9241),
    'NOR': (8.4689, 60.4720),
    'DNK': (9.5018, 56.2639),
    'BEL': (4.4699, 50.5039),
    'AUT': (14.5501, 47.5162),
    'CZE': (15.4730, 49.8175),
    'RUS': (105.3188, 61.5240),
    'CHN': (104.1954, 35.8617),
    'KOR': (127.7669, 35.9078),
    'MEX': (-102.5528, 23.6345),
    'NZL': (174.8860, -40.9006),
    'IRL': (-8.2439, 53.4129),
    'PRT': (-8.2245, 39.3999),
    'GRC': (21.8243, 39.0742),
    'HUN': (19.5033, 47.1625),
    'SGP': (103.8198, 1.3521),
    'ARG': (-63.6167, -38.4161),
    'CHL': (-71.5430, -35.6751),
    'THA': (100.9925, 15.8700),
    'TWN': (120.9605, 23.6978),
    'HKG': (114.1095, 22.3964),
    'ZAF': (22.9375, -30.5595),
}

# Add coordinates
df['Longitude'] = df['ISO3'].map(lambda x: centroids.get(x, (0, 0))[0])
df['Latitude'] = df['ISO3'].map(lambda x: centroids.get(x, (0, 0))[1])

# Save
df.to_csv('cleaned/speedrun_country_agg.csv', index=False)
print("✓ Added coordinates!")