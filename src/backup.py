"""Automated backup (Non-Functional Requirement: Data Backup).
Usage: python src/backup.py  -> database/backups/earthscape_backup_<date>.sql + .db copy"""
import sqlite3, pathlib, datetime, shutil
BASE=pathlib.Path(__file__).resolve().parents[1]; DB=BASE/"database"/"earthscape.db"
out=BASE/"database"/"backups"; out.mkdir(parents=True, exist_ok=True)
stamp=datetime.date.today().isoformat()
shutil.copy(DB, out/f"earthscape_{stamp}.db")
with open(out/f"earthscape_{stamp}.sql","w") as f:
    con=sqlite3.connect(DB)
    for line in con.iterdump(): f.write(line+"\n")
print(f"Backup written: earthscape_{stamp}.db + .sql")
