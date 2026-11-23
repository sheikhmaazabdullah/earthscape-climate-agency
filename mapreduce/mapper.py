#!/usr/bin/env python3
"""Hadoop Streaming mapper: CSV line -> station<TAB>YYYY-MM<TAB>temp,rain,1
Run locally:  cat data/raw/climate_records.csv | python mapreduce/mapper.py | sort | python mapreduce/reducer.py
Run on Hadoop: hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input /earthscape/raw -output /earthscape/monthly"""
import sys
for line in sys.stdin:
    p=line.strip().split(",")
    if len(p)<5 or p[0]=="date": continue
    try: print(f"{p[1]}\t{p[0][:7]}\t{float(p[3])},{float(p[4])},1")
    except ValueError: continue
