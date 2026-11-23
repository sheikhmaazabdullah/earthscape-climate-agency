# Replicating the storage layer on real Hadoop (single-node)
hdfs dfs -mkdir -p /earthscape/raw /earthscape/processed
hdfs dfs -put data/raw/climate_records.csv /earthscape/raw/
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files mapreduce/mapper.py,mapreduce/reducer.py -mapper mapper.py -reducer reducer.py \
  -input /earthscape/raw -output /earthscape/monthly
hdfs dfs -cat /earthscape/monthly/part-00000 | head
# MongoDB (Compass): create DB earthscape, collection climate_records, Import -> data/raw/climate_records.csv
# Impala: CREATE EXTERNAL TABLE monthly (...) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LOCATION '/earthscape/monthly';
