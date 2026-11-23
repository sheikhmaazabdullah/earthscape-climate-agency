# EarthScape — Verified Results (run 21 Nov 2026)

Dataset: 9,135 daily records, 5 stations, 2020-01-01 to 2024-12-31. Missing temperature values in raw data: 137 (handled by station-median imputation at ingestion).

## Anomaly detection (headline set: z-score > 3 per station-month — identical on every machine)
IsolationForest runs as a second, independent detector (column anomaly_iso) for comparison; on a standard Anaconda install it flags ~1% of records, and the union of both detectors was 120 records in the Windows verification run on 21 Nov 2026. The headline count below is the reproducible z-score set used in the report and dashboard.
- Islamabad: 8 anomalies
- Karachi: 5 anomalies
- Lahore: 6 anomalies
- Peshawar: 7 anomalies
- Quetta: 4 anomalies
- TOTAL: 30 anomalies

## Warming trend forecast (least-squares linear trend, per station)
- Islamabad: +0.135 °C per year
- Karachi: +0.065 °C per year
- Lahore: +0.173 °C per year
- Peshawar: +0.169 °C per year
- Quetta: +0.206 °C per year

## Correlation matrix (all stations)
```
               temperature_c  rainfall_mm  humidity_pct  co2_ppm
temperature_c           1.00        -0.36         -0.71     0.26
rainfall_mm            -0.36         1.00          0.29     0.01
humidity_pct           -0.71         0.29          1.00    -0.02
co2_ppm                 0.26         0.01         -0.02     1.00
```
Key readings: temperature vs humidity -0.71 (hotter days are drier), temperature vs rainfall -0.36, temperature vs CO2 +0.26.

## Threshold alerts (temp >= 42°C, rainfall >= 100mm, CO2 >= 430ppm): 578 alerts in total.

## MapReduce (Hadoop Streaming): 300 monthly aggregates = 5 stations x 60 months (2020-2024).