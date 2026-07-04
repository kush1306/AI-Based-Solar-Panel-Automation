import sys; sys.path.insert(0,'src')
from data_loader import load_full_dataset

print("Loading real Delhi dataset...")
df = load_full_dataset(local_path='data/delhi_openmeteo_hourly.csv')
print(f"Rows: {len(df):,}  Cols: {list(df.columns)}")
print(f"Date range: {df['time'].min().date()} -> {df['time'].max().date()}")
print(f"Avg demand: {df['demand_kw'].mean():.3f} kW")
print(f"Daily avg:  {df['demand_kw'].sum()/df['time'].dt.date.nunique():.2f} kWh/day")
print(f"\nSample (summer peak day):")
peak = df[df['time'].dt.strftime('%Y-%m-%d') == '2024-05-15'][['time','temperature_2m','shortwave_radiation','demand_kw']].head(6)
print(peak.to_string(index=False))
