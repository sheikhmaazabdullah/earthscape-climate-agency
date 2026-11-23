"""Ingestion: CSV/JSON -> validation -> missing-data handling -> partitioned storage (HDFS layout)."""
import pandas as pd, pathlib, time, logging
BASE = pathlib.Path(__file__).resolve().parents[1]
REQ = ["date","station","temperature_c","rainfall_mm","humidity_pct","co2_ppm"]
def load(path):
    p = pathlib.Path(path); t=time.time()
    df = pd.read_csv(p) if p.suffix==".csv" else pd.read_json(p)
    missing = [c for c in REQ if c not in df.columns]
    if missing: raise ValueError(f"Missing columns: {missing}")
    df["date"]=pd.to_datetime(df["date"], errors="coerce"); df=df.dropna(subset=["date"])
    before=len(df)
    for c in ["temperature_c","rainfall_mm","humidity_pct","co2_ppm"]:
        df[c]=pd.to_numeric(df[c], errors="coerce")
        df[c]=df.groupby("station")[c].transform(lambda s: s.fillna(s.median()))  # graceful missing-data handling
    logging.info(f"Ingested {before:,} rows in {time.time()-t:.2f}s")
    return df
def write_partitioned(df, root=None):
    root = pathlib.Path(root or BASE/"data"/"hdfs_sim"); n=0
    df=df.copy(); df["y"]=df["date"].dt.year; df["m"]=df["date"].dt.month
    for (y,m,st), g in df.groupby(["y","m","station"]):
        d=root/f"year={y}"/f"month={m:02d}"/f"station={st}"; d.mkdir(parents=True, exist_ok=True)
        g.drop(columns=["y","m"]).to_csv(d/"part-00000.csv", index=False); n+=1
    return n
if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    df=load(BASE/"data"/"raw"/"climate_records.csv"); print(f"Partitions written: {write_partitioned(df)}")
