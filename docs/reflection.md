# Reflection

1. What was the hardest part of setting up the environment, and how did you resolve it?

The hardest part of setting up the environment was a port conflict on 5432. A local PostgreSQL service installed directly on Windows was already listening on that port, so my Python script kept connecting to the wrong database and failing authentication for the dss150p user. I resolved it by checking which processes were using port 5432 with netstat and tasklist, then remapping the Docker container to port 5433 instead of uninstalling or touching the existing Postgres install.

2. Comparing how CSV, JSON, Parquet, the REST API, and PostgreSQL felt to work with, which source felt most "production-ready" and which felt riskiest to build a pipeline on? Why?

Comparing all the sources, orders.json felt the riskiest because of its nested shipping object, which actually broke my profiling script when checking for duplicates. It requires extra handling before it can be treated like a normal flat table. products.parquet felt the most production-ready, since it had zero duplicates and zero missing values across all 200 rows, making it the cleanest source I worked with.

3. If this were a real production pipeline, what is the first data-quality check you would automate, and why that one first?

If this were a real production pipeline, the first data-quality checks I would automate are duplicate detection and null checks, starting with customers.csv. Duplicate customer records can silently inflate metrics like customer counts or revenue per customer, and missing values in fields like email can break downstream processes that assume every record is complete. Catching both early, right at ingestion, prevents bad data from propagating into every later stage of the pipeline.

4. What would you do differently if you repeated this lab?

If I repeated this lab, I would read through the profiling script more carefully before running it, so I could anticipate edge cases like nested JSON fields ahead of time instead of discovering them through a crash.