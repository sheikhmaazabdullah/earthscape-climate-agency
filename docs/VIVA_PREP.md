# EarthScape — Viva Preparation (answers are grounded in YOUR project — use these numbers)
Verified figures: 9,135 records · 5 stations · 2020–2024 · 300 partitions · 300 monthly aggregates ·
30 anomalies (z-score set) · 578 alerts · Karachi +0.065 °C/yr · 13/13 tests.

1. **What is Hadoop / HDFS?** A distributed framework for storing and processing big data across
   machines. HDFS splits files into blocks, replicates them for fault tolerance, and stores them
   across nodes. We mirror its layout with year/month/station partitions and give the real
   single-node HDFS commands in docs/HDFS_COMMANDS.md.
2. **What does MapReduce do in your project?** Mapper emits station + year-month with temp/rain;
   reducer aggregates to monthly average temperature and total rainfall — 300 outputs.
   We use Hadoop Streaming, so the jobs are Python, not Java.
3. **Why Hadoop Streaming?** It lets any language be mapper/reducer; identical code runs locally
   and on a cluster, which is how we developed on Windows without a cluster.
4. **Batch vs real-time?** MapReduce = batch (historical). The stream simulator = real-time
   (1 reading/sec, rolling average, instant alert check). The dashboard merges both views.
5. **How does anomaly detection work?** Z-score per station AND month (threshold 3). Per-year
   scoring was rejected: seasonal swings are ~10 °C, so a heatwave hides inside normal summer
   variation. Per-month scoring found 30 anomalies. IsolationForest is a second detector.
6. **Which ML models?** Least-squares linear regression for warming trend (per station),
   z-score + IsolationForest for anomalies, Pearson correlation for relationships.
7. **What did you find?** All stations warming (+0.065 to +0.206 °C/yr); temp vs humidity −0.71;
   temp vs CO₂ +0.26; 578 threshold alerts (42 °C / 100 mm / 430 ppm).
8. **How is missing data handled?** 137 missing temperatures (1.5%) are imputed with the
   station median at ingestion — documented, never silently dropped.
9. **Where does real data come from?** Open-Meteo Archive API (free, no key) — the fetcher
   pulled 1,827 real Karachi rows. The bundled 9,135-row set is synthetic with a fixed seed
   so results are reproducible; that assumption is stated in the ReadMe.
10. **Security?** Role-based login (Admin/Analyst/Viewer), role checks per page, passwords are configured through environment variables (never stored in code) and hashed (SHA-256) in the database.
11. **Database?** SQLite by default so it runs anywhere (users, stations, climate_records,
    alerts, support_tickets), with a dated backup (.db + .sql) and a MongoDB JSON export
    for MongoDB Compass.
12. **Why Streamlit / Tableau?** Streamlit = fastest interactive Python dashboard, native
    Windows, no Docker. Tableau Public views are built from the MapReduce CSV output.
13. **Scalability?** Add a station or a year = add partitions; MapReduce parallelises by key.
    Nothing in the pipeline hardcodes the 5 stations.
14. **Limitations (say them before the examiner finds them)?** Single-node Hadoop, synthetic
    main dataset, satellite data is satellite-derived tables (not raw imagery), linear (not
    deep-learning) forecasts.
15. **Your role / group?** Built as a five-member group eProject — know the pipeline end to end
    and be able to explain every figure above from your own run.
