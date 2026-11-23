"""Build the EarthScape SQLite database (also exportable to MongoDB via the JSON export).
Creates: users, stations, climate_records, alerts, support_tickets. Populates from the raw CSV."""
import sqlite3, pathlib, sys, json, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
import pandas as pd
from alerts import check as check_alerts
BASE=pathlib.Path(__file__).resolve().parents[1]; DB=BASE/"database"/"earthscape.db"
if DB.exists(): DB.unlink()
con=sqlite3.connect(DB); cur=con.cursor()
cur.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, role TEXT);
CREATE TABLE stations(station_id INTEGER PRIMARY KEY, name TEXT UNIQUE, latitude REAL, longitude REAL);
CREATE TABLE climate_records(record_id INTEGER PRIMARY KEY, station_id INTEGER REFERENCES stations, date TEXT, source TEXT, temperature_c REAL, rainfall_mm REAL, humidity_pct REAL, co2_ppm REAL);
CREATE TABLE alerts(alert_id INTEGER PRIMARY KEY, station TEXT, date TEXT, type TEXT, message TEXT);
CREATE TABLE support_tickets(ticket_id INTEGER PRIMARY KEY, username TEXT, message TEXT, status TEXT DEFAULT 'Open');
""")
# No accounts are seeded with credentials. Optionally set EARTHSCAPE_ADMIN_PASSWORD etc. in the
# environment before running this script to create hashed accounts for those roles.
import os
for role in ("admin","analyst","viewer"):
    pw=os.environ.get(f"EARTHSCAPE_{role.upper()}_PASSWORD")
    if pw: cur.execute("INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",(role,hashlib.sha256(pw.encode()).hexdigest(),role))
coords={"Karachi":(24.86,67.0),"Lahore":(31.55,74.34),"Islamabad":(33.73,73.09),"Quetta":(30.18,66.99),"Peshawar":(34.01,71.58)}
for name,(la,lo) in coords.items(): cur.execute("INSERT INTO stations(name,latitude,longitude) VALUES(?,?,?)",(name,la,lo))
sid={r[1]:r[0] for r in cur.execute("SELECT station_id,name FROM stations")}
df=pd.read_csv(BASE/"data"/"raw"/"climate_records.csv")
for _,r in df.iterrows():
    cur.execute("INSERT INTO climate_records(station_id,date,source,temperature_c,rainfall_mm,humidity_pct,co2_ppm) VALUES(?,?,?,?,?,?,?)",
        (sid[r.station],r.date,r.source,None if pd.isna(r.temperature_c) else r.temperature_c,r.rainfall_mm,r.humidity_pct,r.co2_ppm))
for date,station,typ,msg in check_alerts(df.fillna(0)):
    cur.execute("INSERT INTO alerts(station,date,type,message) VALUES(?,?,?,?)",(station,str(date)[:10],typ,msg))
con.commit()
counts={t:cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ["users","stations","climate_records","alerts"]}
print("DB built:",counts)
# MongoDB-ready export
df.to_json(BASE/"database"/"climate_records_mongo_export.json",orient="records")
con.close()
