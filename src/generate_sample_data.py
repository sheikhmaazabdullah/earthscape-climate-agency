"""Generate realistic synthetic climate data (seeded, reproducible).
Stations: Karachi, Lahore, Islamabad, Quetta, Peshawar (weather-station + sensor + satellite-derived CO2).
Output: data/raw/climate_records.csv  columns used across the whole project."""
import numpy as np, pandas as pd, pathlib
rng = np.random.default_rng(42)
stations = {
 "Karachi":   dict(base=30, amp=6, rain=8,  co2=418),
 "Lahore":    dict(base=27, amp=10, rain=45, co2=422),
 "Islamabad": dict(base=23, amp=9, rain=90, co2=415),
 "Quetta":    dict(base=20, amp=11, rain=18, co2=412),
 "Peshawar":  dict(base=25, amp=10, rain=35, co2=416),
}
rows=[]
dates = pd.date_range("2020-01-01","2024-12-31",freq="D")
for name,s in stations.items():
    seasonal = s["amp"]*np.sin(2*np.pi*(dates.dayofyear.values-100)/365)
    warming = 0.04*((dates - dates[0]).days/365)  # long-term warming trend
    temp = s["base"]+seasonal+warming+rng.normal(0,2.2,len(dates))
    rain = np.maximum(0, rng.gamma(1.2, s["rain"]/12, len(dates)) + (seasonal< -2)*rng.gamma(1,10,len(dates)))
    hum = np.clip(65 - (temp-s["base"])*1.5 + rng.normal(0,8,len(dates)), 15, 100)
    co2 = s["co2"] + 2.2*((dates-dates[0]).days/365) + rng.normal(0,1.2,len(dates))
    df = pd.DataFrame(dict(date=dates, station=name, source=rng.choice(["weather_station","sensor","satellite"],len(dates),p=[.6,.25,.15]),
        temperature_c=np.round(temp,2), rainfall_mm=np.round(rain,2), humidity_pct=np.round(hum,1), co2_ppm=np.round(co2,2)))
    rows.append(df)
data = pd.concat(rows).sort_values(["date","station"]).reset_index(drop=True)
# inject ~1.5% missing values + a few true anomalies (heatwaves / cloudbursts) for ML to find
idx = data.sample(frac=0.015, random_state=1).index; data.loc[idx,"temperature_c"]=np.nan
anom = data.sample(25, random_state=7).index; data.loc[anom,"temperature_c"]+= rng.normal(9,2,25)
anom2 = data.sample(15, random_state=9).index; data.loc[anom2,"rainfall_mm"]+= rng.normal(120,30,15)
out = pathlib.Path(__file__).resolve().parents[1]/"data"/"raw"/"climate_records.csv"
out.parent.mkdir(parents=True, exist_ok=True); data.to_csv(out,index=False)
print(f"Wrote {len(data):,} rows -> {out}")
