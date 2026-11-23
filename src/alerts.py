"""Configurable threshold alerts (spec: Notifications and Alerts)."""
THRESHOLDS = dict(temp_c=42.0, rainfall_mm=100.0, co2_ppm=430.0)
def check(df, th=THRESHOLDS):
    out=[]
    for _,r in df.iterrows():
        if r.temperature_c>=th["temp_c"]: out.append((r.date,r.station,"HEAT",f"{r.temperature_c}°C"))
        if r.rainfall_mm>=th["rainfall_mm"]: out.append((r.date,r.station,"FLOOD_RISK",f"{r.rainfall_mm}mm rain"))
        if r.co2_ppm>=th["co2_ppm"]: out.append((r.date,r.station,"CO2",f"{r.co2_ppm}ppm"))
    return out
