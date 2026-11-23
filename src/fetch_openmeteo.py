"""REAL data option: Open-Meteo Archive API (free, no key) — Karachi daily 2020-2024.
Usage: python src/fetch_openmeteo.py  -> data/raw/openmeteo_karachi.csv"""
import requests, pandas as pd, pathlib
url="https://archive-api.open-meteo.com/v1/archive"
params=dict(latitude=24.86, longitude=67.0, start_date="2020-01-01", end_date="2024-12-31",
            daily="temperature_2m_mean,precipitation_sum,relative_humidity_2m_mean", timezone="Asia/Karachi")
d=requests.get(url, params=params, timeout=60).json()["daily"]
df=pd.DataFrame(d).rename(columns={"time":"date","temperature_2m_mean":"temperature_c",
    "precipitation_sum":"rainfall_mm","relative_humidity_2m_mean":"humidity_pct"})
df["station"]="Karachi"; df["source"]="weather_station"; df["co2_ppm"]=420.0
out=pathlib.Path(__file__).resolve().parents[1]/"data"/"raw"/"openmeteo_karachi.csv"; df.to_csv(out,index=False)
print(f"Wrote {len(df):,} real rows -> {out}")
