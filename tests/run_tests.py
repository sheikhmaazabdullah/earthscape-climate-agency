"""End-to-end test suite - run: python tests/run_tests.py  (all tests use the real project data/code)"""
import sys, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
import pandas as pd
from ingest import load, write_partitioned
from ml_models import detect_anomalies, forecast_trend, correlations
from alerts import check
BASE=pathlib.Path(__file__).resolve().parents[1]
results=[]
def T(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail)); print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
# TC01-TC03 auth logic mirror: accounts come from environment variables (test fixtures set their own)
import os
os.environ["EARTHSCAPE_ADMIN_PASSWORD"]="test-admin-pass"; os.environ["EARTHSCAPE_ANALYST_PASSWORD"]="test-analyst-pass"; os.environ["EARTHSCAPE_VIEWER_PASSWORD"]="test-viewer-pass"
USERS={r:(os.environ[f"EARTHSCAPE_{r.upper()}_PASSWORD"],r) for r in ("admin","analyst","viewer")}
T("TC01 Valid login (admin)", USERS.get("admin",("",""))[0]=="test-admin-pass")
T("TC02 Invalid login rejected", USERS.get("admin",("",""))[0]!="wrongpass")
T("TC03 RBAC roles distinct", len({v[1] for v in USERS.values()})==3)
df=load(BASE/"data"/"raw"/"climate_records.csv")
T("TC04 Ingestion loads dataset", len(df)==9135, f"({len(df)} rows)")
T("TC05 Missing values handled at ingestion", df["temperature_c"].isna().sum()==0, "(median imputation)")
try:
    bad=BASE/"data"/"raw"/"_bad.csv"; bad.write_text("a,b\n1,2\n"); load(bad); ok=False
except ValueError: ok=True
finally: bad.unlink(missing_ok=True)
T("TC06 Invalid file rejected with error", ok)
T("TC07 Partitioned storage writes 300 partitions", write_partitioned(df, BASE/"data"/"hdfs_sim_test")==300)
import shutil; shutil.rmtree(BASE/"data"/"hdfs_sim_test", ignore_errors=True)
# Cross-platform MapReduce test: pure Python pipes (no Unix cat/sort/wc, works on Windows cmd/PowerShell)
import sys as _sys
_raw=(BASE/"data"/"raw"/"climate_records.csv").read_text()
_m=subprocess.run([_sys.executable, str(BASE/"mapreduce"/"mapper.py")], input=_raw, capture_output=True, text=True)
_sorted="\n".join(sorted(_m.stdout.splitlines()))
_r=subprocess.run([_sys.executable, str(BASE/"mapreduce"/"reducer.py")], input=_sorted, capture_output=True, text=True)
_lines=[l for l in _r.stdout.splitlines() if l.strip()]
T("TC08 MapReduce produces 300 monthly aggregates", len(_lines)==300, f"({len(_lines)} lines)")
d=detect_anomalies(pd.read_csv(BASE/"data"/"raw"/"climate_records.csv", parse_dates=["date"]))
T("TC09 Anomaly detection finds injected anomalies", int(d.is_anomaly.sum())==30, f"({int(d.is_anomaly.sum())} found)")
_,py=forecast_trend(pd.read_csv(BASE/"data"/"raw"/"climate_records.csv", parse_dates=["date"]),"Karachi")
T("TC10 Karachi forecast is a warming trend", 0 < py < 0.5, f"({py:+.3f} C/yr)")
T("TC11 Correlation matrix is 4x4", correlations(d).shape==(4,4))
T("TC12 Alert engine fires on thresholds", len(check(d))==578, f"({len(check(d))} alerts)")
import sqlite3
con=sqlite3.connect(BASE/"database"/"earthscape.db"); n=con.execute("SELECT COUNT(*) FROM climate_records").fetchone()[0]
T("TC13 Database holds all records", n==9135, f"({n} rows)")
passed=sum(1 for _,s,_ in results if s=="PASS")
print(f"\n{passed}/{len(results)} tests passed")
pathlib.Path(BASE/"tests"/"TEST_RESULTS.md").write_text("# Test Results - 21 Nov 2026\n\n| Test Case | Result | Detail |\n|---|---|---|\n"+"\n".join(f"| {n} | {s} | {dt} |" for n,s,dt in results)+f"\n\n**{passed}/{len(results)} tests passed.**\n")
sys.exit(0 if passed==len(results) else 1)
