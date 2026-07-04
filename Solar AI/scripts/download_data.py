import sys
sys.path.insert(0, 'src')
from data_loader import download_from_openmeteo

df = download_from_openmeteo(save_path='data/delhi_openmeteo_hourly.csv')
if df is not None:
    print(f"Downloaded: {len(df)} rows")
    print(f"Range: {df['time'].min()} to {df['time'].max()}")
    print(df.head(3).to_string())
else:
    print("Download failed — will use synthetic fallback")
