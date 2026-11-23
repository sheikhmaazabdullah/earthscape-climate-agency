@echo off
REM EarthScape - one-click demo runner for Windows (viva / video day)
REM Double-click, or run from PowerShell:  .\run_demo.bat
echo === 1/5 Generating data ===
python src\generate_sample_data.py
echo === 2/5 Ingestion + partitioned storage ===
python src\ingest.py
echo === 3/5 MapReduce (Hadoop Streaming, local mode) ===
cmd /c "type data\raw\climate_records.csv | python mapreduce\mapper.py | sort | python mapreduce\reducer.py > data\processed\monthly_summary.txt"
echo MapReduce done - 300 monthly aggregates in data\processed\monthly_summary.txt
echo === 4/5 Building database ===
python database\build_db.py
echo === 5/5 Tests ===
python tests\run_tests.py
echo.
echo === Launching dashboard at http://localhost:8501 ===
streamlit run app.py
pause
