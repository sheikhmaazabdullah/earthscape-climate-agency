# Test Results - 21 Nov 2026

| Test Case | Result | Detail |
|---|---|---|
| TC01 Valid login (admin) | PASS |  |
| TC02 Invalid login rejected | PASS |  |
| TC03 RBAC roles distinct | PASS |  |
| TC04 Ingestion loads dataset | PASS | (9135 rows) |
| TC05 Missing values handled at ingestion | PASS | (median imputation) |
| TC06 Invalid file rejected with error | PASS |  |
| TC07 Partitioned storage writes 300 partitions | PASS |  |
| TC08 MapReduce produces 300 monthly aggregates | PASS | (300 lines) |
| TC09 Anomaly detection finds injected anomalies | PASS | (30 found) |
| TC10 Karachi forecast is a warming trend | PASS | (+0.065 C/yr) |
| TC11 Correlation matrix is 4x4 | PASS |  |
| TC12 Alert engine fires on thresholds | PASS | (578 alerts) |
| TC13 Database holds all records | PASS | (9135 rows) |

**13/13 tests passed.**
