"""ML: anomaly detection (per station-month z-score; IsolationForest as independent 2nd detector), trend forecast, correlations.
Core methods use numpy/pandas only, so the project runs even without scikit-learn;
when sklearn is present (standard Anaconda install) IsolationForest is added automatically."""
import pandas as pd, numpy as np
try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
def detect_anomalies(df):
    df=df.copy()
    # Per station AND month: a yearly z-score would hide real anomalies inside seasonal swings
    df["_m"]=df["date"].dt.month
    g=df.groupby(["station","_m"])["temperature_c"]
    df["temp_z"]=(df["temperature_c"]-g.transform("mean"))/g.transform("std")
    df=df.drop(columns=["_m"])
    df["anomaly_z"]=df["temp_z"].abs()>3
    df["anomaly_iso"]=False
    if HAS_SKLEARN:
        iso=IsolationForest(contamination=0.01, random_state=42)
        df["anomaly_iso"]=iso.fit_predict(df[["temperature_c","rainfall_mm","humidity_pct","co2_ppm"]].fillna(0))==-1
    # Headline anomaly set = z-score set ONLY, so results are identical on every machine.
    # IsolationForest (anomaly_iso) is kept as a second, independent detector for comparison;
    # its count varies slightly with the sklearn version, so it never feeds is_anomaly.
    df["is_anomaly"]=df["anomaly_z"]
    return df
def forecast_trend(df, station, days=365):
    d=df[df.station==station].dropna(subset=["temperature_c"]).copy(); d["t"]=(d["date"]-d["date"].min()).dt.days
    slope, intercept = np.polyfit(d["t"], d["temperature_c"], 1)  # least-squares linear trend
    ft=np.arange(d["t"].max()+1, d["t"].max()+1+days)
    future=pd.DataFrame({"t":ft, "predicted_temp_c": slope*ft+intercept})
    future["date"]=d["date"].max()+pd.to_timedelta(future["t"]-d["t"].max(), unit="D")
    return future, float(slope*365)  # warming per year
def correlations(df):
    return df[["temperature_c","rainfall_mm","humidity_pct","co2_ppm"]].corr(numeric_only=True)
