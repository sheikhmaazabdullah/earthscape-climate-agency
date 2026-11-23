#!/usr/bin/env python3
"""Hadoop Streaming reducer: aggregates to monthly avg temp + total rainfall per station."""
import sys
cur=None; st=sr=n=0
def emit():
    if cur: print(f"{cur[0]}\t{cur[1]}\tavg_temp={st/n:.2f}\ttotal_rain={sr:.1f}\tdays={n}")
for line in sys.stdin:
    station, ym, vals = line.strip().split("\t"); t,r,c = vals.split(",")
    key=(station,ym)
    if key!=cur and cur is not None: emit(); st=sr=n=0
    cur=key; st+=float(t); sr+=float(r); n+=int(c)
emit()
